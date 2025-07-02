# FastAPI resumo de texto 
# Autor Sergio Tabarez

# --- Imports Necessários ---
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import json 
import torch

# --- Configuração do FastAPI ---
app = FastAPI(
    title="API de Resumo de Textos com LLM",
    description="API para resumir textos utilizando um modelo de linguagem.",
    version="0.1.0"
)

# --- Modelos de Dados (Schemas) ---
class TextToSummarize(BaseModel):
    text: str

class SummaryResult(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: float

# --- LLM Manager ---
class LLMManager:
    _instance = None # Para implementar o padrão Singleton
    model = None
    tokenizer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMManager, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        print("Carregando o modelo para resumo de texto...")
        model_name = "sshleifer/distilbart-cnn-12-6"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained( 
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        print(f"Modelo {model_name} carregado com sucesso!")


    def generate_summary(self, text: str) -> SummaryResult:
        print("DEBUG: Entrando em generate_summary.")
        
        prompt = "summarize: " + text
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=self.tokenizer.model_max_length,
            truncation=True
        ).to(self.model.device)

        try:
            summary_ids = self.model.generate(
                inputs["input_ids"],
                num_beams=4,
                min_length=30,
                max_length=150,
                early_stopping=True,
                no_repeat_ngram_size=2
            )
            print("DEBUG: Geração do resumo concluída.")
        except Exception as llm_gen_e:
            print(f"ERRO CRÍTICO NA GERAÇÃO DO LLM: {llm_gen_e}")
            return SummaryResult(
                summary="Erro na geração do resumo.",
                original_length=len(text),
                summary_length=0,
                compression_ratio=0.0
            )

        summary_text = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        print(f"DEBUG: Resumo gerado: {summary_text[:200]}...")

        original_len = len(text)
        summary_len = len(summary_text)
        compression = (1 - (summary_len / original_len)) * 100 if original_len > 0 else 0

        return SummaryResult(
            summary=summary_text,
            original_length=original_len,
            summary_length=summary_len,
            compression_ratio=round(compression, 2)
        )

# Inicializa o LLMManager como um Singleton
llm_manager = LLMManager()

# --- Endpoints da API ---
@app.get("/")
async def read_root():
    return {"message": "Bem-vindo à API de Resumo de Textos com LLM!"}

@app.post("/summarize/", response_model=SummaryResult)
async def summarize_text_endpoint(input_text: TextToSummarize):
    print("DEBUG: Requisição recebida no endpoint /summarize/.")
    print(f"Recebida solicitação para resumir texto (início): {input_text.text[:100]}...")

    # Chamar o LLMManager para gerar o resumo
    summary_output = llm_manager.generate_summary(input_text.text)

    print("DEBUG: Retornando resumo.")
    return summary_output

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",  
        port=8000,
        log_level="debug"
    )

