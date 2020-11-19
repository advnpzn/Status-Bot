from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,CommandHandler,CallbackContext, CallbackQueryHandler
import requests
import os
INSULT_URL = os.environ.get("insult_url","")
STATUS_MSG = "Status : NONE"
PM_STATUS = "Can you PM me? : Not Yet Decided"
ADMIN_USER_ID = os.environ.get("admin_userid")

def insult(update: Update, context: CallbackContext) -> None:
  insult = requests.get(INSULT_URL).json()
  update.message.reply_text(insult['insult'],quote=False)

def status(update: Update , context: CallbackContext) -> None:
    update.message.reply_text("{}\n{}".format(STATUS_MSG,PM_STATUS))

def set(update: Update , context: CallbackContext) -> None:
    pmKeyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("✅",callback_data="✅"),
                            InlineKeyboardButton("❌",callback_data="❌"),
                            InlineKeyboardButton("Cancel",callback_data='1'),
                        ]
                    ]
                    )
    if update.message.from_user.id == ADMIN_USER_ID:
        word = ""
        for i in range ( 0, len(context.args), 1 ):
            word = word + "{} ".format(context.args[i])
        global STATUS_MSG
        STATUS_MSG = word
        update.message.reply_text("Your Status :\n{} ".format(STATUS_MSG),reply_markup = pmKeyboard)
    else:
        update.message.reply_text("You don't have enough Credentials to Use this Command!")

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("See the status of what @ATPnull is doing right now!\nYou get BLOCKED if you disturb while \nHe's doing concentrating on other stuff.\nSo, PM him only if he's Free.\ni.e. When the PM status is ✅\nDon't PM when the PM status is ❌\nPress /status to get started\nHave a Nice Day :)")

def pmSTATS(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data != '1':
        global STATUS_MSG
        global PM_STATUS
        STATUS_MSG = "Status : \n{}".format(STATUS_MSG)
        PM_STATUS = "Can you PM me ? : {}".format(query.data)
        query.edit_message_text("Status Updated Successfully!")
    else:
        query.edit_message_text("Status Update Cancelled.")

def main():
    BOT_TOKEN = os.environ.get("token","")
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("status", status,run_async=True))
    dp.add_handler(CommandHandler("set", set,run_async=True))
    dp.add_handler(CommandHandler("help", help,run_async=True))
    dp.add_handler(CommandHandler("insult",insult,run_async=True))
    dp.add_handler(CallbackQueryHandler(pmSTATS))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()



