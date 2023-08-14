import telegram.ext
from process import ask, append_interaction_to_chat_log
from sklearn.metrics.pairwise import cosine_similarity
import logging, os

PORT = int(os.environ.get('PORT', '8443'))

with open('token.txt', 'r') as f:
    TOKEN = str(f.read())

session = {}

def evaluate_response(generated_response, actual_response):
    # Calculate the cosine similarity between the generated and actual responses
    embeddings = openai.Embedding.create([generated_response, actual_response])
    embeddings = np.array(embeddings.embeddings)
    cosine_sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return cosine_sim

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("Hello! Welcome to HealthGuardBot")

def help(update, context):
    update.message.reply_text("""
    The Following commands are available:
    /start -> Welcome to HealthGuard
    /help ->This Message
    /about -> About  HealthGuardBot
    /contact -> Developer Info
    """)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', context.error)

def about(update, context):
    update.message.reply_text("""
            HealthGuardBot is not just a chatbot. It's so much more than that. It's an AI-enabled customer service solution that answers your questions, responds to your tweets, and helps you find the products you're looking for. HealthGuardBot has the power to save you time, increase your sales, and make your customer service operation more efficient.
        """)

def contact(update, context):
    update.message.reply_text("Developer: Divya, Jayoti \n")

def handle_message(update, context):
    chat_log = session.get('chat_log')
    answer = ask(update.message.text, chat_log)

    print(update.message.text)
    print(chat_log)

    # Evaluate the response using the cosine similarity metric
    #evaluation_score = evaluate_response(answer, )
    #print(f"Cosine Similarity Score: {evaluation_score}")


    session['chat_log'] = append_interaction_to_chat_log(update.message.text, answer, chat_log)
    update.message.reply_text(str(answer))

def main():
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    bot = updater.dispatcher

    bot.add_handler(telegram.ext.CommandHandler("start", start))
    bot.add_handler(telegram.ext.CommandHandler("help", help))
    bot.add_handler(telegram.ext.CommandHandler("about", about))
    bot.add_handler(telegram.ext.CommandHandler("contact", contact))
    bot.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

    bot.add_error_handler(error)
    updater.start_polling()


if __name__ == '__main__':
    main()
