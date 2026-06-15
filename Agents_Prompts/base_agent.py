import logging
from abc import ABC, abstractmethod

# Log sistemini alt sınıflar için hazırla
logger = logging.getLogger("Antigravity.BaseAgent")

class BaseAgent(ABC):
    """
    Antigravity Çoklu Ajan Sistemi için Soyut Temel Sınıf (Abstract Base Class).
    Tüm alt ajanlar bu sınıftan türetilmek zorundadır.
    """
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt

    @abstractmethod
    def process(self, memory):
        """
        Her ajanın kendine özel analiz mantığını barındıracağı ana fonksiyon.
        Alt sınıflar bu fonksiyonu ezmek (override etmek) zorundadır.
        """
        pass

    def log_start(self, memory):
        """Tüm ajanların ortak kullanacağı standart başlangıç logu"""
        message = f"[{self.name}] Analiz süreci başlatıldı..."
        memory.add_log(message)

    def log_end(self, memory):
        """Tüm ajanların ortak kullanacağı standart bitiş logu"""
        message = f"[{self.name}] Analiz başarıyla tamamlandı ve hafıza güncellendi."
        memory.add_log(message)