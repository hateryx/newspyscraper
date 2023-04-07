import app as app
from app import soup_getter, content_getter, title_builder, generate_news_pdf


def test_soup_getter():
    assert soup_getter("https://news.abs-cbn.com/news", "news") != []
    assert soup_getter("https://news.abs-cbn.com/business", "business") != []


def test_content_getter():
    assert content_getter(case_1_url) != []


def test_title_builder():
    assert title_builder(case_1_title) == case_1_news_header


def test_generate_news_pdf():
    assert generate_news_pdf(
        case_1_news_header[0], case_1_news_header[1], case_1_list) == "Success"


case_1_url = "https://news.abs-cbn.com/news/02/17/23/dfa-76-notes-protests-sent-to-china-under-marcos-jr"
case_1_list = ["MANILA — President Ferdinand Marcos, Jr.'s administration has so far filed 76 diplomatic notes and protests against China amid tensions in the West Philippine Sea, the Department of Foreign Affairs (DFA) said on Friday.\xa0", 'Manila sends notes and protests to Beijing "every time there is an illegal intrusion or action that\'s actually been committed in our EEZ (exclusive economic zone)," said DFA Spokesperson Teresita Daza.', '"Ang DFA po almost regular na nagpo-protest kasi ho marami pong illegal na action na nangyari… Importante po na maging vigilant kami and through diplomatic action be able to say that they should not continue, this is violative of international law, and they should actually all actions that do not escalate tensions between our waters," she said in a televised briefing.\xa0', '(The DFA protests almost regularly because many illegal actions have taken place. It is important that we stay vigilant.)\xa0', 'The tally included 9 notes sent to China this year, said the official.\xa0', "The DFA has yet to collate data on Beijing's response, Daza said.\xa0", '<strong>DIRECT COMMUNICATION\xa0</strong>', "Manila recently protested a Chinese security vessel's use of military-grade laser against a Philippine patrol boat near Ayungin Shoal in the Spratly Islands on Feb. 6.\xa0", 'The incident came just weeks after President Ferdinand Marcos Jr. and his Chinese counterpart Xi Jinping agreed in January to set up <a href="https://news.abs-cbn.com/news/12/29/22/philippines-china-to-ink-deal-for-direct-communication-on-west-ph-sea">direct communication</a> between their foreign ministries to avoid "miscommunication" in the area.',
               'The Chinese government used this mechanism on Feb. 14 to give its account of the laser incident, said Daza.\xa0', '"Sa atin naman, ni-narrate din po natin kung anong nangyari and how we considered the incident as aggressive and threatening and also we hoped that this actually does not continue. \'Yan ang nangyari sa first use ng communication mechanism," she said.\xa0', "(For our part, we narrated what happened and how we considered the incident as aggressive and threatening... That's what happened in the first use of the communication mechanism.)", 'The official said she hoped Beijing would take "concrete action" on Manila\'s "different calls and protests."\xa0', '"Mayroon namang existing forms of engagement between the 2 countries. Gagamitin \'yun at gagamitin itong communication mechanism," she said.\xa0', "The laser incident incident occurred days after the United States and the Philippines agreed to resume joint patrols in the sea and struck a deal to give US troops access to another 4 military bases in the Southeast Asian country amid China's military rise in the region.", 'Vietnam, Malaysia and Brunei also have overlapping claims to parts of the South China Sea.\xa0', '<strong>— With a report from Agence France-Presse</strong>']

case_1_title = "/news/02/17/23/dfa-76-notes-protests-sent-to-china-under-marcos-jr"
case_1_news_header = (
    "Dfa 76 Notes Protests Sent to China Under Marcos Jr", "February 17, 2023, Friday")
