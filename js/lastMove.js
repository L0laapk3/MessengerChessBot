var person = $("strong.actor:contains('FBChess'):last").parent();
var text = person.parent().parent().find("[data-sigil='message-text']").text();
var att = person.parent().parent().find("div.messageAttachments");
var subtext = att.find("header > :eq(1)").text();
var img = att.find("i").css("backgroundImage");
var match = img.match(/(?=.*fen=([^&]*))(?=.*side=(w|b))/);
var result = {
    fen: match[1],
    side: match[2],
    active: text.contains("(White)") ? "w" : "b",
    turn: parseInt(subtext),
    last: subtext.split(" ")[1]
};
result