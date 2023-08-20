from typing import Final
from telegram import Update
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
import mysql.connector

TOKEN = 'Your BotFather Token Here...'
BOT_USERNAME: Final = '@itampeed_bot'

# MySQL database setup
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySqlpassword@77890",
    database="quiz_app"
)
mycursor = mydb.cursor()

# States for the conversation
ANSWERING = 1

# Retrieve questions from the questions table
def retrieve_questions():
    select_query = "SELECT question, option1, option2, option3, option4, correct FROM questions"
    mycursor.execute(select_query)
    questions_data = mycursor.fetchall()
    return questions_data

# Start the quiz
async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.message.chat_id, text="The quiz is starting...")
    context.user_data['questions_data'] = retrieve_questions()
    context.user_data['total_questions'] = len(context.user_data['questions_data'])
    context.user_data['correct_answers'] = 0
    await send_question(update, context)
    return ANSWERING

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_data = context.user_data['questions_data'][context.user_data['correct_answers']]
    question, option1, option2, option3, option4, correct_answer = question_data
    await context.bot.send_message(chat_id=update.message.chat_id, text=question)
    await context.bot.send_message(chat_id=update.message.chat_id, text="1. " + option1)
    await context.bot.send_message(chat_id=update.message.chat_id, text="2. " + option2)
    await context.bot.send_message(chat_id=update.message.chat_id, text="3. " + option3)
    await context.bot.send_message(chat_id=update.message.chat_id, text="4. " + option4)
    return ANSWERING

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer_text = update.message.text
    print('Check_answer')

    if user_answer_text.isdigit() and 1 <= int(user_answer_text) <= 4:
        user_answer = int(user_answer_text)
        correct_answer = context.user_data['questions_data'][context.user_data['correct_answers']][5]
        print(f"Answer provided: {user_answer}")
        
        if user_answer == correct_answer:
            context.user_data['correct_answers'] += 1

        if context.user_data['correct_answers'] < context.user_data['total_questions']:
            await send_question(update, context)
        else:
            await end_quiz(update, context)  # Return ConversationHandler.END here
    else:
        await context.bot.send_message(chat_id=update.message.chat_id, text="Invalid answer. Please enter a number between 1 and 4.")
        await send_question(update, context)

async def end_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... Calculate and store quiz result in the database ...
    await context.bot.send_message(chat_id=update.message.chat_id, text="Quiz completed!")
    return ConversationHandler.END  # Return ConversationHandler.END here

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print("The quiz just Started, Good Luck !!")
    # Create a bot instance using the token
    bot = Bot(token=TOKEN)
    
    # Create the Application using the bot instance
    app = Application.builder().bot(bot).build()

    # Commands
    app.add_handler(CommandHandler('start', start_quiz))

    # Errors
    app.add_error_handler(error)

    # Polling
    app.run_polling(poll_interval=1)

    # Close MySQL connection when polling ends
    mycursor.close()
    mydb.close()
