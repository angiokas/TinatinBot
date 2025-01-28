from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from pydantic import BaseModel, Field
from typing import Annotated
from discord.ext import commands


MODEL_NAME = "EleutherAI/gpt-neo-125M"
tokenizer = tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

class GenerationConfig(BaseModel):
    max_length: int = Field(..., gt=0)  
    temperature: float = Field(..., ge=0.0, le=1.0)  
    top_p: float = Field(..., ge=0.0, le=1.0)  
    top_k: int = Field(..., gt=0) 
    num_return_sequences: int = Field(..., ge=1)  
    truncation: bool = True  
    do_sample: bool = True

default_config = GenerationConfig(
    max_length=100, 
    temperature=0.9, 
    top_p=0.9, 
    top_k=50,
    num_return_sequences= 1,
    truncation=True,
    do_sample = True
)

class LLM(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.command()
    async def generate_text(self,ctx, prompt: str, config: GenerationConfig = default_config) -> str:
        generation_params = config.model_dump()
        result = generator(prompt, **generation_params)
        generated_text = result[0]["generated_text"]

        await ctx.send(generated_text)
    
    