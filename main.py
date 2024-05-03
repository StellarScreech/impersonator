import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

# Load the fine-tuned language model
model = GPT2LMHeadModel.from_pretrained('path')
tokenizer = GPT2Tokenizer.from_pretrained('path')

# Set up the Telegram bot
updater = Updater(token='7001975986:AAHI5xGjffk6kpVGZWqxvk9IL7ADlm4RtsQ', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm an AI bot that can imitate a specific person. Send me a message and I'll try to respond like them.")

def imitate(update, context):
    # Generate a response using the fine-tuned language model
    input_text = update.message.text
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output_ids = model.generate(input_ids, max_length=100, num_return_sequences=1, do_sample=True, top_k=50, top_p=0.95, num_beams=5)[0]
    output_text = tokenizer.decode(output_ids, skip_special_tokens=True)

    context.bot.send_message(chat_id=update.effective_chat.id, text=output_text)

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(filters.text & ~filters.command, imitate)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()