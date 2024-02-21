// script from https://github.com/fnielsen/scholia/blob/b40962a2e8bd6a3dd3612d16253f14571e8426f6/scholia/app/templates/base.html


// https://stackoverflow.com/questions/6020714
function escapeHTML(html) {
    if (typeof html !== "undefined") {
        return html
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }
    else {
        return "";
    }
}

$('#searchterm').keyup(function (e) {
    var q = $('#searchterm').val();
    $.getJSON("https://www.wikidata.org/w/api.php?callback=?", {
        search: q,
        action: "wbsearchentities",
        language: "en",
        uselang: "en",
        format: "json",
        strictlanguage: true,
    },
        function (data) {
            $("#searchresult").empty();
            $.each(data.search, function (i, item) {
                console.log(item);
                $("#searchresult")
                    .append("<div><a href='/search/" + item.id + "'>" +
                        escapeHTML(item.label) +
                        "</a> - " + escapeHTML(item.description) + "</div>");
            });
        });
});
