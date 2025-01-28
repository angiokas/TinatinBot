import subprocess
import discord
from discord.ext import commands, voice_recv
import wave
from datetime import datetime
import asyncio

class Voice(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.is_recording = False
        self.ffmpeg_process = None
        self.voice_client = None
        self.output_file = None
        self.wavesink = None

    @commands.command()
    async def join_vc(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You need to join a voice channel first!")
            return
        
        self.vc_channel = ctx.author.voice.channel
        self.voice_client = await self.vc_channel.connect(cls=voice_recv.VoiceRecvClient)
        await ctx.send(f"Joined {self.voice_client.channel.name} voice channel.")
        
    @commands.command()
    async def leave_vc(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("I am not connected to a voice channel.")
            return

        await ctx.voice_client.disconnect()
        await ctx.send("I have left the voice channel.")

    @commands.command()
    async def start_recording(self, ctx):
        if self.voice_client is None:
            await ctx.send("I need to be connected to a voice channel to record.")
            return
        
        if self.is_recording:
            await ctx.send("Already recording!")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_file = f"audio_{timestamp}.wav"
        self.is_recording = True

        await ctx.send("Started recording audio!")
        f = open(self.output_file, 'wb')
        self.sink = voice_recv.WaveSink(f)
        #self.sink = lambda user, data: print(f"{user}")
        self.voice_client.listen(self.sink)
            
    
    #Stops recording and prompts the user if they want the audio saved. 
    @commands.command()
    async def stop_recording(self, ctx):

        if not self.is_recording:
            await ctx.send("I am not currently recording.")
            return
        
        self.is_recording = False
        self.voice_client.stop_listening()        
        await ctx.send(f"Stopped recording. Audio saved to {self.output_file}.")

async def setup(bot):
    await bot.add_cog(Voice(bot))