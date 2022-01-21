# the summary generator has ben split into two functions. 
# The first function "transcription" gives the transcript of the video, taking the file path of the video as the input. 
# The second function "summary", which takes the transcript as its input, calls the openai API and generates the summary of the transcript.
# The output of the "transcription" function is a string of the transcript which is then used as the input for the "summary" function
# Since we are running the transcription by parts, it is best if we call the transcription function for each part and then combine the
# transcripts of the individual parts. The combined transcript can then be used as the input for the "summary" function, which gives
# the summary as a string.


import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import openai


def transcription(filepath):
  transcribed_audio_file_name = "transcribed_speech.wav"
  audioclip = AudioFileClip(filepath)
  audioclip.write_audiofile(transcribed_audio_file_name)
  # create a speech recognition object
  r = sr.Recognizer()

  # a function that splits the audio file into chunks
  # and applies speech recognition
  def get_large_audio_transcription(path):
      """
      Splitting the large audio file into chunks
      and apply speech recognition on each of these chunks
      """
      # open the audio file using pydub
      sound = AudioSegment.from_wav(path)  
      # split audio sound where silence is 700 miliseconds or more and get chunks
      chunks = split_on_silence(sound,
          # experiment with this value for your target audio file
          min_silence_len = 500,
          # adjust this per requirement
          silence_thresh = sound.dBFS-14,
          # keep the silence for 1 second, adjustable as well
          keep_silence=500,
      )
      folder_name = "audio-chunks"
      # create a directory to store the audio chunks
      if not os.path.isdir(folder_name):
          os.mkdir(folder_name)
      whole_text = ""
      # process each chunk 
      for i, audio_chunk in enumerate(chunks, start=1):
          # export audio chunk and save it in
          # the `folder_name` directory.
          chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
          audio_chunk.export(chunk_filename, format="wav")
          # recognize the chunk
          with sr.AudioFile(chunk_filename) as source:
              audio_listened = r.record(source)
              # try converting it to text
              try:
                  text = r.recognize_google(audio_listened)
              except sr.UnknownValueError as e:
                  print("Error:", str(e))
              else:
                  text = f"{text.capitalize()}. "
                  print(chunk_filename, ":", text)
                  whole_text += text
      # return the text for all chunks detected
      return whole_text
  return get_large_audio_transcription("transcribed_speech.wav")    
    

def summary(transcript):
  openai.api_key = "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"
  ans = transcript
  ans = ans + "///"
  response = openai.Completion.create(engine="davinci",prompt=ans,temperature=0.3,
              max_tokens=50,
              top_p=0.8,
              frequency_penalty=0,
              presence_penalty=0,
              stop=["///"]
          )

  return response["choices"][0]["text"]
