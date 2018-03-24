#!/usr/bin/env python3
import time
import logging
import json
import subprocess
import datetime

from telegram.ext.dispatcher import run_async
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import telegram

from datetime import datetime

from wbdconf import *
updater = Updater(token=ttoken)
dispatcher = updater.dispatcher

ver = 'v0.1.25318'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def help(bot, update):
    write_log(update.message.from_user, "help", "command")

    output = "<strong>walletbotd </strong>" + ver + " running " + "<strong>" + coinname + "</strong>"
    output += "\n\nCommand list:\n\n"
    output += "/info - get generic information about your wallet,\n\n"
    output += "/wallet - display active accounts in your wallet,\n\n"
    output += "/account - display detailed info about an account,\n"
    output += "\t `/account myaccount1`\n\n"
    output += "/newaccount - create a new account in your wallet,\n"
    output += "\t `/newaccount mynewaccount2`\n\n"
    output += "/unlock - unlocks your wallet for two minutes to send coins,\n"
    output += "\t `/unlock mysupersecretwalletpassword`\n\n"
    output += "/send - send " + coinname + " from automatically selected inputs,\n"
    output += "\t `/send Mpr3zWUEZrowiKC5dwJanq5faenUzR613L 100000`\n\n"
    output += "/advsend - send " + coinname + " from a specific account,\n"
    output += "\t `/advsend myaccount2 Mpr3zWUEZrowiKC5dwJanq5faenUzR613L 100000`\n\n"
    output += "/move - move " + coinname + \
        " from a specific account to another within your wallet,\n"
    output += "\t `/move myaccount1 myaccount2 100000`\n\n"
    output += "/help - this helper you see right now.\n\n"
    output += "\n\n\nCredits @enlil0 (telegram) \n https://github.com/nexus166/walletbotd"

    bot.send_message(chat_id=update.message.chat_id,
                     text=output, parse_mode=telegram.ParseMode.HTML)


def write_log(user, query, query_type):
    name = user.first_name if user.first_name != None else ''
    last_name = user.last_name if user.last_name != None else ''
    username = user.username if user.username != None else ''

    with open("logs", "a") as logs:
        line = str(datetime.now()) + "\t"
        line += (" first name: " + name + "; last name: " + last_name + "; username: " +
                 username + "; query: " + query + "; querytype: " + query_type + "\n")
        logs.write(line)
        print(line)


def info(bot, update):
    write_log(update.message.from_user, "info", "command")

    if owner == update.message.from_user.username:
        result = subprocess.run(
            [coind, "getinfo"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = json.loads(result.stdout.strip().decode('utf-8'))

        output = "<strong>walletbotd </strong>" + ver + "\n"
        output += coinname + ' wallet ' + str(result['version']) + "\n\n"
        output += "\t" + "<strong>Protocol Version:  </strong>" + str(result['protocolversion']) + "\n"
        output += "\t" + "<strong>Wallet Version:  </strong>" + str(result['walletversion']) + "\n"
        output += "\t" + "<strong>On TestNet:  </strong>" + str(result['testnet']) + "\n"
        output += "\t" + "<strong># of connections:  </strong>" + str(result['connections']) + "\n"
        output += "\t" + "<strong>Proxy:  </strong>" + str(result['proxy']) + "\n\n"

        output += "<strong>Minting</strong>\n"
        output += "\t" + "<strong>Blocks:  </strong>" + str(result['blocks']) + "\n"
        output += "\t" + "<strong>Total supply:  </strong>" + str(result['moneysupply']) + "\n"
        output += "\t" + "<strong>Minted coins:  </strong>" + str(result['newmint']) + "\n"
        output += "\t" + "<strong>Stake:  </strong>" + str(result['stake']) + "\n"
        output += "\t" + "<strong>Difficulty(PoS):  </strong>" + str(result['difficulty']) + "\n\n\n"

        bot.send_message(chat_id=update.message.chat_id,
                         text=output, parse_mode=telegram.ParseMode.HTML)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="UNAUTHORIZED")


def wallet(bot, update):
    write_log(update.message.from_user, "myaccounts", "command")

    if owner == update.message.from_user.username:
        result = subprocess.run(
            [coind, "listreceivedbyaddress"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = json.loads(result.stdout.strip().decode('utf-8'))

        output = ''
        for acc in result[:]:
            accdetails = "<strong>Name: </strong>" + acc['account'] + "\n" + "<strong>Balance: </strong>" + str(
                acc['amount']) + ' ' + coinname + "\n" + "<strong>Address: </strong>" + acc['address'] + "\n\n"
            output += accdetails

        bot.send_message(chat_id=update.message.chat_id,
                         text=output, parse_mode=telegram.ParseMode.HTML)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="UNAUTHORIZED")


def account(bot, update):
    write_log(update.message.from_user, "account", "command")
    cmd = update.message.text.split(' ')[0:]

    if owner == update.message.from_user.username:
        try:
            balance = subprocess.run(
                [coind, "getbalance", cmd[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            balance = (balance.stdout.strip()).decode("utf-8")
            addresses = subprocess.run(
                [coind, "getaddressesbyaccount", cmd[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            addresses = json.loads(addresses.stdout.strip().decode('utf-8'))
            last3tx = subprocess.run(
                [coind, "listtransactions", cmd[1], '3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            last3tx = json.loads(last3tx.stdout.strip().decode('utf-8'))
        except subprocess.CalledProcessError as e:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Something went wrong.. Try with another account?')

        output = "<strong>Account report for </strong>" + cmd[1] + "\n\n"
        output += "<strong>Balance: </strong>" + \
            str(balance) + ' ' + coinname + "\n\n"
        output += "<strong>Addresses</strong>" + "\n"
        for addr in addresses:
            output += "\t" + addr + "\n"
        output += "\n" + "<strong>Last 3 transactions</strong>" + "\n"

        for tx in last3tx[:]:
            txtime = time.strftime('%Y-%m-%d %H:%M:%S',
                                   time.localtime(tx['time'])) + ' UTC'

            txamount = ''
            if (tx['category'] == 'receive'):
                txamount += '+'
                txid = tx['txid']
            elif (tx['category'] == 'send'):
                txamount += '-'
                txid = tx['txid']
            elif (tx['category'] == 'move'):
                txid = "(moved to " + tx['otheraccount'] + ')'
            txamount += str(tx['amount']) + ' ' + coinname

            output += txtime + ' ' + txid + ' ' + txamount + "\n\n"

        bot.send_message(chat_id=update.message.chat_id,
                         text=output, parse_mode=telegram.ParseMode.HTML)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="UNAUTHORIZED")


def newaccount(bot, update):
    write_log(update.message.from_user, "newaccount", "command")
    cmd = update.message.text.split(' ')[0:]

    if owner == update.message.from_user.username:
        try:
            result = subprocess.run(
                [coind, "getnewaddress", cmd[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = (result.stdout.strip()).decode("utf-8")
            output = "Account " + cmd[1] + " created." + \
                "\n" + "New address: " + result + "\n"
            bot.send_message(chat_id=update.message.chat_id, text=output)
        except subprocess.CalledProcessError as e:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Wrong syntax! Try again (/newaccount accountname)')
    else:
        bot.send_message(chat_id=update.message.chat_id, text="UNAUTHORIZED")


def unlock(bot, update):
    write_log(update.message.from_user, "unlock", "command")
    cmd = update.message.text.split(' ')[0:]

    if owner == update.message.from_user.username:
        try:
            unlockresult = subprocess.check_output(
                [coind, "walletpassphrase", cmd[1], str(unlock_timeout)], stderr=subprocess.STDOUT)
            output = "Wallet unlocked successfully! You have two minutes to send new transactions."
            bot.send_message(chat_id=update.message.chat_id, text=output)
        except subprocess.CalledProcessError as e:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Wrong passphrase!')
    else:
        bot.send_message(chat_id=update.message.chat_id, text="UNAUTHORIZED")


def send(bot, update):
    write_log(update.message.from_user, "simplesend", "command")
    cmd = update.message.text.split(' ')[0:]

    if owner == update.message.from_user.username:
        try:
            tx = subprocess.run([coind, "sendtoaddress", cmd[1], cmd[2]],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            txid = (tx.stdout.strip()).decode("utf-8")
            errs = (tx.stderr.strip()).decode("utf-8")
            output = "TXID: " + txid + "\n\n"
            output += "Errors: \n" + errs
            bot.send_message(chat_id=update.message.chat_id, text=output)
        except subprocess.CalledProcessError as e:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Something went wrong.\nThings to check:\n\t- is the wallet locked?\n\t- do you have enough coins?")

        bot.send_message(chat_id=update.message.chat_id, text=result)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="UNAUTHORIZED")


def advsend(bot, update):
    write_log(update.message.from_user, "send", "command")
    cmd = update.message.text.split(' ')[0:]
    if owner == update.message.from_user.username:
        try:
            tx = subprocess.run([coind, "sendfrom", cmd[1], cmd[2], cmd[3]],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            txid = (tx.stdout.strip()).decode("utf-8")
            errs = (tx.stderr.strip()).decode("utf-8")
            output = "TXID: " + txid + "\n\n"
            output += "Errors: \n" + errs
            bot.send_message(chat_id=update.message.chat_id, text=output)
        except subprocess.CalledProcessError as e:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Something went wrong.\nThings to check:\n\t- is the wallet locked?\n\t- do you have enough coins?")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="UNAUTHORIZED")


def move(bot, update):
    write_log(update.message.from_user, "move", "command")
    cmd = update.message.text.split(' ')[0:]
    if owner == update.message.from_user.username:
        try:
            tx = subprocess.run([coind, "move", cmd[1], cmd[2], cmd[3]],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            txid = (tx.stdout.strip()).decode("utf-8")
            errs = (tx.stderr.strip()).decode("utf-8")
            output = "TXID: " + txid + "\n\n"
            output += "Errors: \n" + errs
            bot.send_message(chat_id=update.message.chat_id, text=output)
        except subprocess.CalledProcessError as e:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Something went wrong.\nThings to check:\n\t- is the wallet locked?\n\t- do you have enough coins?")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="UNAUTHORIZED")


start_handler = CommandHandler('help', help)
dispatcher.add_handler(start_handler)
start_handler = CommandHandler('info', info)
dispatcher.add_handler(start_handler)
start_handler = CommandHandler('wallet', wallet)
dispatcher.add_handler(start_handler)
start_handler = CommandHandler('account', account)
dispatcher.add_handler(start_handler)
start_handler = CommandHandler('newaccount', newaccount)
dispatcher.add_handler(start_handler)
start_handler = CommandHandler('unlock', unlock)
dispatcher.add_handler(start_handler)
start_handler = CommandHandler('send', send)
dispatcher.add_handler(start_handler)
start_handler = CommandHandler('advsend', advsend)
dispatcher.add_handler(start_handler)
start_handler = CommandHandler('move', move)
dispatcher.add_handler(start_handler)

print(str(datetime.now()) + "\tWBD LISTENING")

updater.start_polling()
 
