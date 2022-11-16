
ddddd



storage = {}

def init_storage(user_id):
  storage[user_id] = dict(first_number=None, second_number=None)

def store_number(user_id, key, value):
  storage[user_id][key] = dict(value=value)

def get_number(user_id, key):
  return storage[user_id][key].get('value')

@bot.message_handler(func=lambda m: True)
def start(message):
 init_storage(message.from_user.id)
 bot.reply_to(message, "What have you forgotten here, traveler? \
 Do you want to play? If you want - write 'Yes', if don't - write 'No'.")
 bot.register_next_step_handler(message, answer)
  
def answer(message):
    if message.text == "Yes":
        bot.reply_to(message,"This is the correct answer. Enter any two numbers, and we will check if\
 the sum of these numbers is a prime number.")
        bot.register_next_step_handler(message, plus_one)
    elif message.text == "No":
        bot.reply_to(message, "The answer is incorrect. You have seven days left. To cancel the curse - write 'Yes'")
        bot.register_next_step_handler(message, answer)
    elif message.text == "/start":
        bot.reply_to(message, "Either answer 'Yes', or click again'/start'!")
        bot.register_next_step_handler(message, start)
    else:
        bot.reply_to(message, "The answer is incorrect. You have seven days left. To cancel the curse - write 'Yes'")
        bot.register_next_step_handler(message, answer)

def plus_one(message):
        first_number = message.text

        if not first_number.isdigit():
            msg = bot.reply_to(message, 'Enter a number, not text!')
            bot.register_next_step_handler(message, plus_one)
            return

        store_number(message.from_user.id, "first_number", first_number)
        bot.reply_to(message, f"Great! The first number = {first_number }. Now enter the second number.")
        bot.register_next_step_handler(message, plus_two)

def plus_two(message):
       second_number = message.text

       if not second_number.isdigit():
            msg = bot.reply_to(message, 'Enter a number, not text! Pay attention!')
            bot.register_next_step_handler(message, plus_two)
            return

       store_number(message.from_user.id, "second_number", second_number)
       
       number_1 = get_number(message.from_user.id, "first_number")
       number_2 = get_number(message.from_user.id, "second_number")

       result_plus = int(number_1) + int(number_2)
       bot.reply_to(message, f"Great! The second number = {second_number}. Total amount: {result_plus}.  Now press '+'")
       bot.register_next_step_handler(message, finish)
       
def finish(message):
    if message.text == "+":
        number_1 = get_number(message.from_user.id, "first_number")
        number_2 = get_number(message.from_user.id, "second_number")
        result_plus = int(number_1) + int(number_2)
        flag = True
        for i in range(2, result_plus // 2 + 1):
            if result_plus % i == 0:
                flag = False
                break  
        if result_plus > 1 and flag == True:
            bot.reply_to(message, f"The game is over. The number is simple. Do you want to play again?")
            bot.register_next_step_handler(message, answer)
        elif result_plus == 1:
            bot.reply_to(message, f"The game is over. The number is not simple, and not composite. This is a unit. Do you want to play again?")
            bot.register_next_step_handler(message, answer)
        elif result_plus == 0:
            bot.reply_to(message, f"The game is over. The number is not simple, and not composite. This is a zero. Do you want to play again?")
            bot.register_next_step_handler(message, answer)
        else:
            bot.reply_to(message, f"The game is over. Composite number. Do you want to play again?")
            bot.register_next_step_handler(message, answer)
            
    else:
        bot.reply_to(message, "The answer is incorrect. You have seven days left. To cancel the curse - press '+'")
        bot.register_next_step_handler(message, finish)



if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
    bot.infinity_polling()
    
    
    
    
    
    
 