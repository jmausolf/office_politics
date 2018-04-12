import textile
from credentials import *

message_text = """Dear (name of Google contact):

I am writing in response to your notice for the Data Scientist, Google Cloud position at your Sunnyvale office. I am a doctoral candidate in Computer Science at Stanford University, specializing in the application of recurrent neural networks in cloud computing. Google is a leader in data science and artificial intelligence, and I am confident, together, we would be a great match.

As a computer scientist, I have both the theoretical knowledge and applied experience to make a difference at Google. As you can see from my resume, I have not only developed enhanced RNN algorithms in Java, but also used Python, Scala, and SQL to apply deep neural nets and streamline ETL pipelines as a data science intern for both Facebook and LinkedIn. Collectively, my background in computer science, statistics, and mathematical modeling gives me first hand experience into the crux of today’s complex computational puzzles in data science and their applications at the frontiers of artificial intelligence.

Although I have strong methodological strengths and my doctoral degree underscores my ability to tackle complex problems, I also strive to work as a team player, whether its by collaborating with colleagues at Facebook and LinkedIn to communicate data-driven solutions or spearheading fundraising initiatives and leading a diverse set of students during my tenure as president of the Harvard Republican Club. I think you will agree that my computational background—combined with my outgoing charisma and penchant for collaborative leadership—makes me a valuable recruit for the data scientist position at Google.

I want you to know that I am excited to submit my application to Google. Attached, please find a copy of my resume. I look forward to speaking with you soon so that we can discuss the position further. 

Warm regards,"""



sig_text = """
{}
{}
{}
C: {} | {}
""".format(name, title, school, phone, gmail_user)

sig_html = """
<div style="background-color:rgb(255,255,255)"><font face="Copperplate" size="3">{}</font>
</div>
<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Copperplate">{}</font>
</div>
<div style="font-family:Tahoma;font-size:13px"><font face="Copperplate" color="#800000" size="3" style="background-color:rgb(255,255,255)">{}</font></div>
<div style="background-color:rgb(255,255,255);font-family:Tahoma;font-size:13px"><font face="Copperplate">C:<span>&nbsp;</span><a href="tel:{}" value="{}" style="color:rgb(17,85,204)" target="_blank">336-948-0756</a><span>&nbsp;</span>|<span>&nbsp;</span><a href="mailto:{}" class="m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967m_197796773055002560m_2319474238175162055dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967m_197796773055002560dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734m_3507498170987872967dly-gmail m_-4756129822142185649gmail-m_4655728448235344902m_170831212088922734dly-gmail m_-4756129822142185649gmail-m_4655728448235344902dly-gmail m_-4756129822142185649gmail-dly-gmail m_-4756129822142185649dly-gmail dly-gmail" style="color:rgb(17,85,204)" target="_blank">{}</a></font></div></div>
""".format(name, title, school, phone, phone_link, gmail_user, gmail_user)


message_html = """<html><div style="color:rgb(0,0,0);font-family:&quot;Times New Roman&quot;,Times,serif,Times,EmojiFont,&quot;Apple Color Emoji&quot;,&quot;Segoe UI Emoji&quot;,NotoColorEmoji,&quot;Segoe UI Symbol&quot;,&quot;Android Emoji&quot;,EmojiSymbols;font-size:16px;font-style:normal;font-variant-ligatures:normal;font-variant-caps:normal;font-weight:400;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;background-color:rgb(255,255,255);text-decoration-style:initial;text-decoration-color:initial">{}{}</div></html>
""".format(textile.textile( message_text ), sig_html)
print(message_html)