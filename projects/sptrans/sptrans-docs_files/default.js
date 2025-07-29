ativaTab = 1;

//https://github.com/FabioVergani/js-Polyfill_String-trimStart
(function (w) {
    var String = w.String, Proto = String.prototype;

    (function (o, p) {
        if (p in o ? o[p] ? false : true : true) {
            var r = /^\s+/;
            o[p] = o.trimLeft || function () {
                return this.replace(r, '')
            }
        }
    })(Proto, 'trimLeft');

})(window);

/* Equipe SIM
Baseado na solução https://github.com/FabioVergani/js-Polyfill_String-trimStart
*/
(function (w) {
    var String = w.String, Proto = String.prototype;

    (function (o, p) {
        if (p in o ? o[p] ? false : true : true) {
            var r = /\s+$/;
            o[p] = o.trimEnd || function () {
                return this.replace(r, '')
            }
        }
    })(Proto, 'trimEnd');

})(window);

//https://github.com/FabioVergani/js-Polyfill_String-trimStart
(function (w) {
    var String = w.String, Proto = String.prototype;

    (function (o, p) {
        if (p in o ? o[p] ? false : true : true) {
            var r = /^\s+/;
            o[p] = o.trimLeft || function () {
                return this.replace(r, '')
            }
        }
    })(Proto, 'trimStart');

})(window);



$(document).ready(function () {
    
    $("h1").children("a").children("img").attr("alt","Logo da SPTrans");
    $("h1").children("a").children("img").attr("title","Logo da SPTrans");

    $(":input").focus(function () {        
        $(document).unbind("keydown");        
    })

    $(document).bind("keydown", "window", function (e) {        
        var keyCode = e.keyCode || e.which;
        if (keyCode == 9) {            
            e.preventDefault();
            // call custom function here
            $("#accessibility").removeAttr("class");
            $(".nav-accessibility a[accesskey='1']").focus();
            $(this).unbind("keydown");
        }
    }); 
		
		
	$( "a[target='_blank']").click(function(e){
	    console.log($(this).attr("href"));
        gtag('event', 'Acesso', { event_category: 'Link Externo', event_action: "Click", event_label: $(this).attr("href")});
	})

});

