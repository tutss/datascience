var urlApiInfotrans = "//itinerariosapi.sptrans.com.br/";

window.TodasLinhas;


var listPontosDefinidos = {};
//var $dropdownPontoItinerarioOrigem, $dropdownPontoItinerarioDestino, $dropdownPontoItinerarioOrigemSubSelecao, $dropdownPontoItinerarioDestinoSubSelecao,
var $txtEnderecoOrigem, $txtNumeroEnderecoOrigem, $txtCruzamentoInicioOrigem, $txtCruzamentoFinaloOrigem,
    $txtEnderecoDestino, $txtNumeroEnderecoDestino, $txtCruzamentoInicioDestino, $txtCruzamentoFinaloDestino,
    $btnBuscarTrajeto, $btnContinuarCruzamento, $btnContinuarBuscarTrajeto, $btnVoltarBuscarTrajeto,
    $chkLinhasAcessiveis, $chkMetro, $chkCPTM, $selectFaixaHoraria, $selectDiaUtil, $selectPrioridade, $txtQueroAndar, $divOptionsOrigem, $divOptionsDestino,
    $btnBuscarItinerarioPorLinha, $dropdownPontoItinerarioDestinoLocal, $dropdownPontoItinerarioOrigemLocal, $btnBuscarLocal,
    $btnContinuarCruzamentoLocal, $btnContinuarBuscarTrajetoLocal, $btnContinuarBuscarLocal, $txtCruzamentoFinaloOrigemLocal,
    $btnVoltarBuscarLocal, $radioPontosDeInteresse;//, $linhaSelecionada;

var linhaSelecionadaBusca;

//#region Loading
function comecaLoading() {
    $("#divLoading").show();
};
function terminaLoading() {
    $("#divLoading").hide();
};
//#endregion Loading
//#region exibicaoDivs
function esconderDivs() {
    $("#divResultados").hide();
    $("#divMensagemErro").hide();
    $("#divMapaTrajeto").hide();
};
function exibirMensagemErro(msgErro) {
    $("#divResultados").show();
    $("#divMensagemErro").show();
    $("#divMapaTrajeto").hide();
    $("#h3MensagemErro").html(msgErro);
};

function RemoveAccents(str) {
  var accents    = 'ÀÁÂÃÄÅàáâãäåÒÓÔÕÕÖØòóôõöøÈÉÊËèéêëðÇçÐÌÍÎÏìíîïÙÚÛÜùúûüÑñŠšŸÿýŽž';
  var accentsOut = "AAAAAAaaaaaaOOOOOOOooooooEEEEeeeeeCcDIIIIiiiiUUUUuuuuNnSsYyyZz";
  str = str.toUpperCase().replace("VL.","VILA");
  str = str.toUpperCase().replace("PQ.","PARQUE");
  str = str.toUpperCase().replace("TERM.","TERMINAL");
  str = str.split('');
  var strLen = str.length;
  var i, x;
  for (i = 0; i < strLen; i++) {
    if ((x = accents.indexOf(str[i])) != -1) {
      str[i] = accentsOut[x];
    }
    
  }
  return str.join('');
}
//#endregion exibicaoDivs

$(document).ready(function () {

    atendimentos1 = null;
    //#region seletores
    $txtEnderecoOrigem = $("#txtEnderecoOrigem");
    $txtNumeroEnderecoOrigem = $("#txtNumeroEnderecoOrigem");
    $txtCruzamentoInicioOrigem = $("#txtCruzamentoInicioOrigem");
    $txtCruzamentoFinaloOrigem = $("#txtCruzamentoFinaloOrigem");
    //$dropdownPontoItinerarioOrigem = $("#selectPontoItinerarioOrigem");
    //$dropdownPontoItinerarioOrigemSubSelecao = $("#selectPontoItinerarioOrigemSubSelecao");

    $txtEnderecoDestino = $("#txtEnderecoDestino");
    $txtNumeroEnderecoDestino = $("#txtNumeroEnderecoDestino");
    $txtCruzamentoInicioDestino = $("#txtCruzamentoInicioDestino");
    $txtCruzamentoFinaloDestino = $("#txtCruzamentoFinaloDestino");
    $dropdownPontoItinerarioDestino = $("#selectPontoItinerarioDestino");
    $dropdownPontoItinerarioDestinoSubSelecao = $("#selectPontoItinerarioDestinoSubSelecao");

    $chkMetro = $("#chkMetro");
    $chkCPTM = $("#chkCPTM");
    //$chkLinhasAcessiveis = $("#chkLinhasAcessiveis");
    $selectFaixaHoraria = $("#selectFaixaHoraria");
    $selectDiaUtil = $("#selectDiaUtil");
    $selectPrioridade = $("#selectPrioridade");
    $txtQueroAndar = $("#txtQueroAndar");

    $btnBuscarTrajeto = $("#btnBuscarTrajeto");
    $btnContinuarBuscarTrajeto = $("#btnContinuarBuscarTrajeto");
    $btnContinuarCruzamento = $("#btnContinuarCruzamento");
    $btnVoltarBuscarTrajeto = $("#btnVoltarBuscarTrajeto");
    $btnBuscarLocal = $("#btnBuscarLocal");
    $btnVoltarBuscarLocal = $("#btnVoltarBuscarLocal");

    $btnContinuarCruzamentoLocal = $("#btnContinuarCruzamentoLocal");
    $btnContinuarBuscarTrajetoLocal = $("#btnContinuarBuscarTrajetoLocal");
    $btnContinuarBuscarLocal = $("#btnContinuarBuscarLocal");

    $divOptionsOrigem = $("#divOptionsOrigem");
    $divOptionsDestino = $("#divOptionsDestino");
    $divOptionsOrigemLocal = $("#divOptionsOrigemLocal");

    $btnBuscarItinerarioPorLinha = $("#btnBuscarItinerarioPorLinha");

    $dropdownPontoItinerarioOrigemLocal = $("#selectPontoItinerarioOrigemLocal");
    $dropdownPontoItinerarioDestinoLocal = $("#selectPontosInteressesDestino");
    $txtEnderecoOrigemLocal = $("#txtEnderecoOrigemLocal");
    $txtNumeroEnderecoOrigemLocal = $("#txtNumeroEnderecoOrigemLocal");
    $txtCruzamentoInicioOrigemLocal = $("#txtCruzamentoInicioOrigemLocal");
    $txtCruzamentoFinaloOrigemLocal = $("#txtCruzamentoFinaloOrigemLocal");
    $dropdownPontoItinerarioOrigemSubSelecaoLocal = $("#selectPontoItinerarioOrigemSubSelecaoLocal");
    $radioPontosDeInteresse = $('input[type=radio][name=grupoRadioPontosDeInteresse]');
    //#endregion seletores

    //buscarPontosDefinidos();
    popularForm();
    buscarLinhas();
    

    //$($dropdownPontoItinerarioOrigem).on('change', function () {

    //    var selecionado = $(this).val();

    //    if (selecionado == "s_01") {
    //        $txtEnderecoOrigem.show();
    //        $txtNumeroEnderecoOrigem.show();
    //        $txtCruzamentoInicioOrigem.hide();
    //        $txtCruzamentoFinaloOrigem.hide();
    //        $dropdownPontoItinerarioOrigemSubSelecao.hide();
    //    } else if (selecionado == "s_02") {
    //        $txtEnderecoOrigem.hide();
    //        $txtNumeroEnderecoOrigem.hide();
    //        $txtCruzamentoInicioOrigem.show();
    //        $txtCruzamentoFinaloOrigem.show();
    //        $dropdownPontoItinerarioOrigemSubSelecao.hide();
    //    } else {
    //        $txtEnderecoOrigem.hide();
    //        $txtNumeroEnderecoOrigem.hide();
    //        $txtCruzamentoInicioOrigem.hide();
    //        $txtCruzamentoFinaloOrigem.hide();
    //        $dropdownPontoItinerarioOrigemSubSelecao.show();
    //        $dropdownPontoItinerarioOrigemSubSelecao.find('option').remove().end();

    //        var pontosSelecionados = listPontosDefinidos[selecionado].pontos;
    //        for (var i = 0; i < pontosSelecionados.length; i++) {
    //            $dropdownPontoItinerarioOrigemSubSelecao.append($("<option />").val(pontosSelecionados[i].cod).text(pontosSelecionados[i].nome));
    //        };
    //    }
    //});

    //$($dropdownPontoItinerarioDestino).on('change', function () {

    //    var selecionado = $(this).val();

    //    if (selecionado == "s_01") {
    //        $txtEnderecoDestino.show();
    //        $txtNumeroEnderecoDestino.show();
    //        $txtCruzamentoInicioDestino.hide();
    //        $txtCruzamentoFinaloDestino.hide();
    //        $dropdownPontoItinerarioDestinoSubSelecao.hide();
    //    } else if (selecionado == "s_02") {
    //        $txtEnderecoDestino.hide();
    //        $txtNumeroEnderecoDestino.hide();
    //        $txtCruzamentoInicioDestino.show();
    //        $txtCruzamentoFinaloDestino.show();
    //        $dropdownPontoItinerarioDestinoSubSelecao.hide();
    //    } else {
    //        $txtEnderecoDestino.hide();
    //        $txtNumeroEnderecoDestino.hide();
    //        $txtCruzamentoInicioDestino.hide();
    //        $txtCruzamentoFinaloDestino.hide();
    //        $dropdownPontoItinerarioDestinoSubSelecao.show();
    //        $dropdownPontoItinerarioDestinoSubSelecao.find('option').remove().end();

    //        var pontosSelecionados = listPontosDefinidos[selecionado].pontos;
    //        for (var i = 0; i < pontosSelecionados.length; i++) {
    //            $dropdownPontoItinerarioDestinoSubSelecao.append($("<option />").val(pontosSelecionados[i].cod).text(pontosSelecionados[i].nome));
    //        };
    //    };
    //});

    $($dropdownPontoItinerarioOrigemLocal).on('change', function () {

        var selecionado = $(this).val();

        if (selecionado == "s_01") {
            $txtEnderecoOrigemLocal.show();
            $txtNumeroEnderecoOrigemLocal.show();
            $txtCruzamentoInicioOrigemLocal.hide();
            $txtCruzamentoFinaloOrigemLocal.hide();
            $dropdownPontoItinerarioOrigemSubSelecaoLocal.hide();
        } else if (selecionado == "s_02") {
            $txtEnderecoOrigemLocal.hide();
            $txtNumeroEnderecoOrigemLocal.hide();
            $txtCruzamentoInicioOrigemLocal.show();
            $txtCruzamentoFinaloOrigemLocal.show();
            $dropdownPontoItinerarioOrigemSubSelecaoLocal.hide();
        } else {
            $txtEnderecoOrigemLocal.hide();
            $txtNumeroEnderecoOrigemLocal.hide();
            $txtCruzamentoInicioOrigemLocal.hide();
            $txtCruzamentoFinaloOrigemLocal.hide();
            $dropdownPontoItinerarioOrigemSubSelecaoLocal.show();
            $dropdownPontoItinerarioOrigemSubSelecaoLocal.find('option').remove().end();

            var pontosSelecionados = listPontosDefinidos[selecionado].pontos;
            for (var i = 0; i < pontosSelecionados.length; i++) {
                $dropdownPontoItinerarioOrigemSubSelecaoLocal.append($("<option />").val(pontosSelecionados[i].cod).text(pontosSelecionados[i].nome));
            };
        };
    });

    $($radioPontosDeInteresse).on('change', function () {
        if ($(this).val() == 'O') {
            $dropdownPontoItinerarioDestinoLocal.prop('disabled', false);
        } else {
            $dropdownPontoItinerarioDestinoLocal.prop('disabled', true);
        };
    });

    $($btnBuscarTrajeto).on('click', function () {


        function trataErroTrajeto(respostaOrigem) {
            console.error('Resposta BuscarEndereco erro. Código: ' + respostaOrigem.codigoErro + '. Mensagem: ' + respostaOrigem.mensagem);
            $("#divSelecaoEnderecos").show('fast',function(){
                $("#divSelecaoEnderecos .filtros-busca-itinerarios").hide();
            });
            $("#pTextoResultados").text('');
            $('label[for="' + $($divOptionsOrigem).prop("id") + '"').hide();
            $($divOptionsOrigem).hide();
            $('label[for="' + $($divOptionsDestino).prop("id") + '"').hide();
            $($divOptionsDestino).hide();
            $($btnContinuarBuscarTrajeto).hide();
            $($btnContinuarCruzamento).hide();
            exibirMensagemErro(respostaOrigem.mensagem);
        };


        var reqOrigem, reqDestino, NomeOrigem, NomeDestino;
        var OrigemNo = 0;
        var DestinoNo = 0;

        $($btnContinuarCruzamento).hide();
        $($btnContinuarBuscarTrajeto).show();

        $("#divFormBuscaTrajeto").hide();
        $("#divFiltros").hide();

        //#region pegaValores

        //origem
        //var selecaoPontoOrigem = $($dropdownPontoItinerarioOrigem).val();
        var selecaoPontoOrigem = "s_01";
        var txtEnderecoOrigem = $($txtEnderecoOrigem).val();
        var txtNumeroEnderecoOrigem = $($txtNumeroEnderecoOrigem).val();
        console.log(txtNumeroEnderecoOrigem);
        if(txtNumeroEnderecoOrigem==""){
            txtNumeroEnderecoOrigem = "100";
        }
        var txtCruzamentoInicioOrigem = $($txtCruzamentoInicioOrigem).val();
        var txtCruzamentoFinaloOrigem = $($txtCruzamentoFinaloOrigem).val();

        //destino
        //var selecaoPontoDestino = $($dropdownPontoItinerarioDestino).val();
        var selecaoPontoDestino = "s_01";
        var txtEnderecoDestino = $($txtEnderecoDestino).val();
        var txtNumeroEnderecoDestino = $($txtNumeroEnderecoDestino).val();
        console.log(txtNumeroEnderecoDestino);
        if(txtNumeroEnderecoDestino==""){
            txtNumeroEnderecoDestino = "100";
        }
        var txtCruzamentoInicioDestino = $($txtCruzamentoInicioDestino).val();
        var txtCruzamentoFinaloDestino = $($txtCruzamentoFinaloDestino).val();

        //filtros
        var chkMetro = ($($chkMetro)[0].checked ? 1 : 0);
        var chkCPTM = ($($chkCPTM)[0].checked ? 1 : 0);
        var chkLinhasAcessiveis = 0;//($($chkLinhasAcessiveis)[0].checked ? 1 : 0);
        var selecaoFaixaHoraria = Number($($selectFaixaHoraria).val());
        var selectDiaUtil = Number($($selectDiaUtil).val());
        var selectPrioridade = $($selectPrioridade).val();
        var txtQueroAndar = Number($($txtQueroAndar).val());
        //#endregion pegaValores

        //#region chamadas Origem
        if (selecaoPontoOrigem && selecaoPontoOrigem != "s_00") {
            if (selecaoPontoOrigem == "s_01") {
                if (!txtEnderecoOrigem.trim() || !txtNumeroEnderecoOrigem.trim()) {
                    exibirMensagemErro('Por favor, preencha os campos "Endereço" e "Nº"');
                    terminaLoading();
                    $("#divFormBuscaTrajeto").show();
                    $("#divFiltros").show();
                    return;
                } else {
                    reqOrigem = buscarEndereco(txtEnderecoOrigem, txtNumeroEnderecoOrigem);
                };
            }
            else if (selecaoPontoOrigem == "s_02") {
                if (!txtCruzamentoInicioOrigem.trim() || !txtCruzamentoFinaloOrigem.trim()) {
                    exibirMensagemErro('Por favor, preencha os campos "Origem Cruzamento" e "Destino Cruzamento"');
                    terminaLoading();
                    $("#divFormBuscaTrajeto").show();
                    $("#divFiltros").show();
                    return;
                } else {
                    reqOrigem = buscarEndereco(txtCruzamentoInicioOrigem, "0");
                };
            }
            //else {
            //    var selecaoSubPontoOrigem = $($dropdownPontoItinerarioOrigemSubSelecao).val();
            //    reqOrigem = verificarGfNosID(selecaoSubPontoOrigem, selecaoPontoOrigem);
            //};
        };
        //#endregion chamadas Origem

        //#region chamadas Destino
        if (selecaoPontoDestino && selecaoPontoDestino != "s_00") {
            if (selecaoPontoDestino == "s_01") {
                if (!txtEnderecoDestino.trim() || !txtNumeroEnderecoDestino.trim()) {
                    exibirMensagemErro('Por favor, preencha os campos "Endereço" e "Nº"');
                    terminaLoading();
                    $("#divFormBuscaTrajeto").show();
                    $("#divFiltros").show();
                    return;
                } else {
                    reqDestino = buscarEndereco(txtEnderecoDestino, txtNumeroEnderecoDestino)
                };
            }
            else if (selecaoPontoDestino == "s_02") {
                if (!txtCruzamentoInicioDestino.trim() || !txtCruzamentoFinaloDestino.trim()) {
                    exibirMensagemErro('Por favor, preencha os campos "Origem Cruzamento" e "Destino Cruzamento"');
                    terminaLoading();
                    $("#divFormBuscaTrajeto").show();
                    $("#divFiltros").show();
                    return;
                } else {
                    reqDestino = buscarEndereco(txtCruzamentoInicioDestino, "0");
                };
            }
            //else {
            //    var selecaoSubPontoDestino = $($dropdownPontoItinerarioDestinoSubSelecao).val();
            //    reqDestino = verificarGfNosID(selecaoSubPontoDestino, selecaoPontoDestino);
            //};
        };
        //#endregion chamadas Destino

        Promise.all([reqOrigem, reqDestino]).then(function () {

            terminaLoading();

            var respostaOrigem = reqOrigem.responseJSON;
            var respostaDestino = reqDestino.responseJSON;

            if (selecaoPontoOrigem == "s_01") {
                if (respostaOrigem) {

                    if (respostaOrigem.codigoErro) {
                        trataErroTrajeto(respostaOrigem);
                        return;

                    } else if (respostaOrigem.length > 1) {

                        $("#divSelecaoEnderecos").show();
                        $("#pTextoResultados").text('Foram encontrados vários resultados para a sua busca. Por favor, selecione abaixo o resultado desejado e clique em "Continuar".');

                        populaDivOptionsSubSelecao($divOptionsOrigem, respostaOrigem, true, false, false);

                    } else if (respostaOrigem.length == 1) {

                        OrigemNo = respostaOrigem[0].identificadorNo;
                        NomeOrigem = respostaOrigem[0].nomeRua + " " + respostaOrigem[0].numeroInicial + " a " + respostaOrigem[0].numeroFinal + ", " + respostaOrigem[0].bairro + ", " + respostaOrigem[0].cep + ' ';
                        populaDivOptionsSubSelecao($divOptionsOrigem, respostaOrigem, true, false, false);
                    };
                };
            }
            else if (selecaoPontoOrigem == "s_02") {

                $($btnContinuarCruzamento).show();
                $($btnContinuarBuscarTrajeto).hide();

                if (respostaOrigem) {

                    if (respostaOrigem.codigoErro) {
                        trataErroTrajeto(respostaOrigem);
                        return;

                    } else if (respostaOrigem.length > 1) {

                        $("#divSelecaoEnderecos").show();
                        $("#pTextoResultados").text('Foram encontrados vários resultados para a sua busca. Por favor, selecione abaixo o resultado desejado e clique em "Continuar".');

                        populaDivOptionsSubSelecao($divOptionsOrigem, respostaOrigem, true, true, false);

                    } else if (respostaOrigem.length == 1) {
                        OrigemNo = respostaOrigem[0].identificadorNo
                        NomeOrigem = respostaOrigem[0].nomeRua + " " + respostaOrigem[0].numeroInicial + " a " + respostaOrigem[0].numeroFinal + ", " + respostaOrigem[0].bairro + ", " + respostaOrigem[0].cep + ' ';
                        populaDivOptionsSubSelecao($divOptionsOrigem, respostaOrigem, true, true, false);
                    };
                };
            }
            else {

                if (respostaOrigem.codigoErro) {
                    trataErroTrajeto(respostaOrigem);
                    return;

                }
                //else {
                //    OrigemNo = respostaOrigem
                //    NomeOrigem = $($dropdownPontoItinerarioOrigemSubSelecao).children("option").filter(":selected").text();
                //    listSelecao = [{ nome: NomeOrigem, identificadorNo: OrigemNo }];
                //    populaDivOptionsSubSelecao($divOptionsOrigem, listSelecao, true, false, true);
                //}

            };

            //destino
            if (selecaoPontoDestino == "s_01") {
                if (respostaDestino) {

                    if (respostaDestino.codigoErro) {
                        trataErroTrajeto(respostaDestino);
                        return;

                    } else if (respostaDestino.length > 1) {

                        $("#divSelecaoEnderecos").show();
                        $("#pTextoResultados").text('Foram encontrados vários resultados para a sua busca. Por favor, selecione abaixo o resultado desejado e clique em "Continuar".');

                        populaDivOptionsSubSelecao($divOptionsDestino, respostaDestino, false, false, false);

                    } else if (respostaDestino.length == 1) {

                        DestinoNo = respostaDestino[0].identificadorNo
                        NomeDestino = respostaDestino[0].nomeRua + " " + respostaDestino[0].numeroInicial + " a " + respostaDestino[0].numeroFinal + ", " + respostaDestino[0].bairro + ", " + respostaDestino[0].cep + ' ';

                        populaDivOptionsSubSelecao($divOptionsDestino, respostaDestino, false, false, false);
                    };
                };
            }
            else if (selecaoPontoDestino == "s_02") {

                $($btnContinuarCruzamento).show();
                $($btnContinuarBuscarTrajeto).hide();

                if (respostaDestino) {

                    if (respostaDestino.codigoErro) {
                        trataErroTrajeto(respostaDestino);
                        return;

                    }else if (respostaDestino.length > 1) {

                        $("#divFormBuscaTrajeto").hide();
                        $("#divFiltros").hide();
                        $("#divSelecaoEnderecos").show();
                        $("#pTextoResultados").text('Foram encontrados vários resultados para a sua busca. Por favor, selecione abaixo o resultado desejado e clique em "Continuar".');

                        populaDivOptionsSubSelecao($divOptionsDestino, respostaDestino, false, true, false);

                    } else if (respostaDestino.length == 1) {
                        DestinoNo = respostaDestino[0].identificadorNo
                        NomeDestino = respostaDestino[0].nomeRua + " " + respostaDestino[0].numeroInicial + " a " + respostaDestino[0].numeroFinal + ", " + respostaDestino[0].bairro + ", " + respostaDestino[0].cep + ' ';
                        populaDivOptionsSubSelecao($divOptionsDestino, respostaDestino, false, true, false);
                    };
                };
            } else {

                if (respostaDestino.codigoErro) {
                    trataErroTrajeto(respostaDestino);
                    return;

                }
                //else {
                //    DestinoNo = respostaDestino
                //    NomeDestino = $($dropdownPontoItinerarioDestinoSubSelecao).children("option").filter(":selected").text();
                //    listSelecao = [{ nome: NomeDestino, identificadorNo: DestinoNo }];
                //    populaDivOptionsSubSelecao($divOptionsDestino, listSelecao, false, false, true);
                //}

            };

            if (OrigemNo != 0 && DestinoNo != 0) {
                if (!(selecaoPontoDestino == "s_02") && !(selecaoPontoOrigem == "s_02")) {
                    montarTrajeto(OrigemNo, DestinoNo, NomeOrigem, NomeDestino);
                } else {
                    $($btnContinuarCruzamento).trigger('click');
                };
            };

        }).catch(function (ex) {
            terminaLoading();
            $("#divFormBuscaTrajeto").show();
            $("#divFiltros").show();
            exibirMensagemErro('Ocorreu um erro, por favor tente novamente.');
            console.error('ERRO promisses: ' + ex);
        });

    });

    $($btnContinuarBuscarTrajeto).on('click', function () {

        //filtros
        var chkMetro = ($($chkMetro)[0].checked ? 1 : 0);
        var chkCPTM = ($($chkCPTM)[0].checked ? 1 : 0);
        var chkLinhasAcessiveis = 0;//($($chkLinhasAcessiveis)[0].checked ? 1 : 0);
        var selecaoFaixaHoraria = Number($($selectFaixaHoraria).val());
        var selectDiaUtil = Number($($selectDiaUtil).val());
        var selectPrioridade = $($selectPrioridade).val();
        var txtQueroAndar = Number($($txtQueroAndar).val());

        var OrigemNo = Number($("input[name='grupoRadioOrigem']:checked").val());
        var DestinoNo = Number($("input[name='grupoRadioDestino']:checked").val());
        var NomeOrigem = $("input[name='grupoRadioOrigem']:checked").attr('datanome');
        var NomeDestino = $("input[name='grupoRadioDestino']:checked").attr('datanome');

        montarTrajeto(OrigemNo, DestinoNo, NomeOrigem, NomeDestino);

    });

    $($btnContinuarCruzamento).on('click', function () {

        $($btnContinuarCruzamento).hide();
        $($btnContinuarBuscarTrajeto).show();
        $("#divFormBuscaTrajeto").hide();
        $("#divFiltros").hide();
        $("#divSelecaoEnderecos").hide();

        var reqOrigemCep, reqDestinoCep, NomeOrigem, NomeDestino;
        var OrigemNo = 0;
        var DestinoNo = 0;

        var OrigemIBGE = $("input[name='grupoRadioOrigem']:checked").val();
        var DestinoIBGE = $("input[name='grupoRadioDestino']:checked").val();

        var txtCruzamentoFinaloOrigem = $($txtCruzamentoFinaloOrigem).val();
        var txtCruzamentoFinaloDestino = $($txtCruzamentoFinaloDestino).val();

        //var selecaoPontoOrigem = $($dropdownPontoItinerarioOrigem).val();
        var selecaoPontoOrigem = "s_01";
        if (selecaoPontoOrigem == "s_02") {
            reqOrigemCep = buscarCruzamento(OrigemIBGE, txtCruzamentoFinaloOrigem);
        } else {
            reqOrigemCep = new Promise(function (res, rej) { res(""); });
            if (selecaoPontoOrigem == "s_01") {

                var valorSelecionado = Number($("input[name='grupoRadioOrigem']:checked").val());
                $divOptionsOrigem.find('.form-check [value!="' + valorSelecionado + '"][for!="rdOr' + valorSelecionado + '"]').remove().end();
                OrigemNo = valorSelecionado;
                NomeOrigem = $("input[name='grupoRadioOrigem']:checked").attr('datanome');

            }
            //else {
            //    var selecaoSubPontoOrigem = $($dropdownPontoItinerarioOrigemSubSelecao).val();
            //    reqOrigemCep = verificarGfNosID(selecaoSubPontoOrigem, selecaoPontoOrigem, 1);
            //};
        };

        //var selecaoPontoDestino = $($dropdownPontoItinerarioDestino).val();
        var selecaoPontoDestino = "s_01";
        if (selecaoPontoDestino == "s_02") {
            reqDestinoCep = buscarCruzamento(DestinoIBGE, txtCruzamentoFinaloDestino);
        } else {
            reqDestinoCep = new Promise(function (res, rej) { res(""); });
            if (selecaoPontoDestino == "s_01") {

                var valorSelecionado = Number($("input[name='grupoRadioDestino']:checked").val());
                $divOptionsDestino.find('.form-check [value!="' + valorSelecionado + '"][for!="rdDs' + valorSelecionado + '"]').remove().end();
                DestinoNo = valorSelecionado;
                NomeDestino = $("input[name='grupoRadioDestino']:checked").attr('datanome');

            }
            //else {
            //    var selecaoSubPontoDestino = $($dropdownPontoItinerarioDestinoSubSelecao).val();
            //    reqDestinoCep = verificarGfNosID(selecaoSubPontoDestino, selecaoPontoDestino, 1);
            //};
        };

        Promise.all([reqOrigemCep, reqDestinoCep]).then(function () {

            terminaLoading();

            if (reqOrigemCep && reqOrigemCep.responseJSON && reqOrigemCep.responseJSON.codigoErro) {
                console.error('Resposta MontarTrajeto erro. Código: ' + reqOrigemCep.responseJSON.codigoErro + '. Mensagem: ' + reqOrigemCep.responseJSON.mensagem);
                exibirMensagemErro(reqOrigemCep.responseJSON.mensagem);
            } else if (reqDestinoCep && reqDestinoCep.responseJSON && reqDestinoCep.responseJSON.codigoErro) {
                console.error('Resposta MontarTrajeto erro. Código: ' + reqDestinoCep.responseJSON.codigoErro + '. Mensagem: ' + reqDestinoCep.responseJSON.mensagem);
                exibirMensagemErro(reqDestinoCep.responseJSON.mensagem);
            } else {

                var respostaOrigem = reqOrigemCep.responseJSON;
                var respostaDestino = reqDestinoCep.responseJSON;

                if (reqOrigemCep.responseJSON && reqDestinoCep.responseJSON && (reqOrigemCep.responseJSON.length == 1) && (reqDestinoCep.responseJSON.length == 1)) {

                    OrigemNo = reqOrigemCep.responseJSON[0].identificadorNo
                    NomeOrigem = respostaOrigem[0].nomeRua + " " + respostaOrigem[0].numeroInicial + " a " + respostaOrigem[0].numeroFinal + ", " + respostaOrigem[0].bairro + ", " + respostaOrigem[0].cep + ' ';
                    DestinoNo = reqDestinoCep.responseJSON[0].identificadorNo
                    NomeDestino = respostaDestino[0].nomeRua + " " + respostaDestino[0].numeroInicial + " a " + respostaDestino[0].numeroFinal + ", " + respostaDestino[0].bairro + ", " + respostaDestino[0].cep + ' ';

                } else {

                    //origem
                    if (reqOrigemCep.responseJSON) {
                        if (reqOrigemCep.responseJSON.length > 1) {

                            $("#divFormBuscaTrajeto").hide();
                            $("#divFiltros").hide();
                            $("#divSelecaoEnderecos").show();
                            $("#pTextoResultados").text('Foram encontrados diversos cruzamentos para a sua busca. Por favor, selecione abaixo o desejado e clique em "Continuar".');

                            populaDivOptionsSubSelecao($divOptionsOrigem, reqOrigemCep.responseJSON, true, false, false);

                        } else if (reqOrigemCep.responseJSON.length == 1) {
                            OrigemNo = reqOrigemCep.responseJSON[0].identificadorNo
                            NomeOrigem = reqOrigemCep.responseJSON[0].nomeRua + " " + reqOrigemCep.responseJSON[0].numeroInicial + " a " + reqOrigemCep.responseJSON[0].numeroFinal + ", " + reqOrigemCep.responseJSON[0].bairro + ", " + reqOrigemCep.responseJSON[0].cep + ' ';
                            populaDivOptionsSubSelecao($divOptionsOrigem, reqOrigemCep.responseJSON, true, false, false);
                        }
                        //else {
                        //    OrigemNo = reqOrigemCep.responseJSON;
                        //    NomeOrigem = $($dropdownPontoItinerarioOrigemSubSelecao).children("option").filter(":selected").text();
                        //};
                    };

                    //destino
                    if (reqDestinoCep.responseJSON) {
                        if (reqDestinoCep.responseJSON.length > 1) {

                            $("#divFormBuscaTrajeto").hide();
                            $("#divFiltros").hide();
                            $("#divSelecaoEnderecos").show();
                            $("#pTextoResultados").text('Foram encontrados diversos cruzamentos para a sua busca. Por favor, selecione abaixo o desejado e clique em "Continuar".');

                            populaDivOptionsSubSelecao($divOptionsDestino, reqDestinoCep.responseJSON, false, false, false);

                        } else if (reqDestinoCep.responseJSON.length == 1) {
                            DestinoNo = reqDestinoCep.responseJSON[0].identificadorNo
                            NomeDestino = reqDestinoCep.responseJSON[0].nomeRua + " " + reqDestinoCep.responseJSON[0].numeroInicial + " a " + reqDestinoCep.responseJSON[0].numeroFinal + ", " + reqDestinoCep.responseJSON[0].bairro + ", " + reqDestinoCep.responseJSON[0].cep + ' ';
                            populaDivOptionsSubSelecao($divOptionsDestino, reqDestinoCep.responseJSON, false, false, false);
                        }
                        //else {
                        //    DestinoNo = reqDestinoCep.responseJSON;
                        //    NomeDestino = $($dropdownPontoItinerarioDestinoSubSelecao).children("option").filter(":selected").text();
                        //};
                    };
                };

                if (OrigemNo != 0 && DestinoNo != 0) {
                    montarTrajeto(OrigemNo, DestinoNo, NomeOrigem, NomeDestino);
                };

            };
        }).catch(function () {
            terminaLoading();
            exibirMensagemErro('ERRO promisses');
            console.error('ERRO promisses');
        });

    });

    $($btnVoltarBuscarTrajeto).on('click', function () {
        $("#divFormBuscaTrajeto").show();
        $("#divFiltros").show();
        $("#divSelecaoEnderecos").hide();
        esconderDivs();
    });

    //$($btnBuscarLocal).on('click', function () {

    //    esconderDivs();

    //    var reqOrigem, NomeOrigem, NomeDestino;
    //    var OrigemNo = 0;
    //    var DestinoNo = 0;

    //    $($btnContinuarCruzamentoLocal).hide();
    //    $($btnContinuarBuscarLocal).show();

    //    $("#divFormBuscaLocal").hide();

    //    //#region pegaValores


    //    //origem
    //    var selecaoPontoOrigem = $($dropdownPontoItinerarioOrigemLocal).val();
    //    var txtEnderecoOrigem = $($txtEnderecoOrigemLocal).val();
    //    var txtNumeroEnderecoOrigem = $($txtNumeroEnderecoOrigemLocal).val();
    //    var txtCruzamentoInicioOrigem = $($txtCruzamentoInicioOrigemLocal).val();
    //    var txtCruzamentoFinaloOrigem = $($txtCruzamentoFinaloOrigemLocal).val();

    //    //#region chamadas Origem
    //    if (selecaoPontoOrigem && selecaoPontoOrigem != "s_00") {
    //        if (selecaoPontoOrigem == "s_01") {
    //            if (!txtEnderecoOrigem || !txtNumeroEnderecoOrigem) {
    //                exibirMensagemErro('Por favor, preencha os campos "Endereço" e "Nº"');
    //                $("#divFormBuscaLocal").show();
    //                return;
    //            } else {
    //                reqOrigem = buscarEndereco(txtEnderecoOrigem, txtNumeroEnderecoOrigem)
    //            };
    //        }
    //        else if (selecaoPontoOrigem == "s_02") {
    //            if (!txtCruzamentoInicioOrigem || !txtCruzamentoFinaloOrigem) {
    //                exibirMensagemErro('Por favor, preencha os campos "Origem Cruzamento" e "Destino Cruzamento"');
    //                $("#divFormBuscaLocal").show();
    //                return;
    //            } else {
    //                reqOrigem = buscarEndereco(txtCruzamentoInicioOrigem, "0");
    //            };

    //        } else {
    //            var selecaoSubPontoOrigem = $($dropdownPontoItinerarioOrigemSubSelecaoLocal).val();
    //            reqOrigem = verificarGfNosID(selecaoSubPontoOrigem, selecaoPontoOrigem);
    //        };
    //    };
    //    //#endregion chamadas Destino

    //    Promise.all([reqOrigem]).then(function () {

    //        terminaLoading();

    //        var respostaOrigem = reqOrigem.responseJSON;

    //        //origem
    //        if (selecaoPontoOrigem == "s_01") {
    //            if (reqOrigem.responseJSON) {

    //                if (reqOrigem.responseJSON.codigoErro) {
    //                    console.error('Resposta BuscarEndereco erro. Código: ' + reqOrigem.responseJSON.codigoErro + '. Mensagem: ' + reqOrigem.responseJSON.mensagem);
    //                    $("#divSelecaoEnderecosLocal").show();
    //                    $("#pTextoResultadosLocal").text('');
    //                    $('label[for="divOptionsOrigemLocal"').hide();
    //                    $($divOptionsOrigemLocal).hide();
    //                    $($btnContinuarCruzamentoLocal).hide();
    //                    $($btnContinuarBuscarLocal).hide();
    //                    exibirMensagemErro(reqOrigem.responseJSON.mensagem);

    //                } else if (reqOrigem.responseJSON.length > 1) {

    //                    $("#divSelecaoEnderecosLocal").show();
    //                    $("#pTextoResultadosLocal").text('Foram encontrados vários resultados para a sua busca. Por favor, selecione abaixo o resultado desejado e clique em "Continuar".');

    //                    populaDivOptionsSubSelecao($divOptionsOrigemLocal, respostaOrigem, true, false, false);

    //                    $($btnContinuarCruzamentoLocal).hide();
    //                    $($btnContinuarBuscarLocal).show();

    //                } else if (reqOrigem.responseJSON.length == 1) {

    //                    OrigemNo = reqOrigem.responseJSON[0].identificadorNo
    //                    NomeOrigem = reqOrigem.responseJSON[0].nomeRua + " " + reqOrigem.responseJSON[0].numeroInicial + " a " + reqOrigem.responseJSON[0].numeroFinal + ", " + reqOrigem.responseJSON[0].bairro + ", " + reqOrigem.responseJSON[0].cep + ' ';
    //                    populaDivOptionsSubSelecao($divOptionsOrigemLocal, respostaOrigem, true, false, false);
    //                };
    //            };
    //        }
    //        else if (selecaoPontoOrigem == "s_02") {

    //            $($btnContinuarCruzamentoLocal).show();
    //            $($btnContinuarBuscarLocal).hide();

    //            if (reqOrigem.responseJSON) {

    //                if (reqOrigem.responseJSON.codigoErro) {
    //                    console.error('Resposta BuscarEndereco erro. Código: ' + reqOrigem.responseJSON.codigoErro + '. Mensagem: ' + reqOrigem.responseJSON.mensagem);
    //                    $("#divSelecaoEnderecosLocal").show();
    //                    $("#pTextoResultadosLocal").text('');
    //                    $('label[for="divOptionsOrigemLocal"').hide();
    //                    $($divOptionsOrigemLocal).hide();
    //                    $($btnContinuarCruzamentoLocal).hide();
    //                    $($btnContinuarBuscarLocal).hide();
    //                    exibirMensagemErro(reqOrigem.responseJSON.mensagem);

    //                } else if (reqOrigem.responseJSON.length > 1) {

    //                    $("#divFormBuscaTrajeto").hide();
    //                    $("#divSelecaoEnderecosLocal").show();
    //                    $("#pTextoResultadosLocal").text('Foram encontrados vários resultados para a sua busca. Por favor, selecione abaixo o resultado desejado e clique em "Continuar".');

    //                    populaDivOptionsSubSelecao($divOptionsOrigemLocal, respostaOrigem, false, true, false);

    //                } else if (reqOrigem.responseJSON.length == 1) {
    //                    OrigemNo = respostaOrigem[0].identificadorNo
    //                    NomeOrigem = respostaOrigem[0].nomeRua + " " + respostaOrigem[0].numeroInicial + " a " + respostaOrigem[0].numeroFinal + ", " + respostaOrigem[0].bairro + ", " + respostaOrigem[0].cep + ' ';
    //                    populaDivOptionsSubSelecao($divOptionsOrigemLocal, respostaOrigem, false, true, false);
    //                };
    //            };
    //        } else {
    //            OrigemNo = reqOrigem.responseJSON
    //            NomeOrigem = $($dropdownPontoItinerarioOrigemSubSelecaoLocal).children("option").filter(":selected").text();
    //        };

    //        if (OrigemNo != 0) {
    //            if (!(selecaoPontoOrigem == "s_02")) {

    //                if ($($radioPontosDeInteresse.selector + ':checked').val() == 'O') {
    //                    DestinoNo = $($dropdownPontoItinerarioDestinoLocal).val();
    //                    NomeDestino = $($dropdownPontoItinerarioDestinoLocal.selector + ' option:selected').text();
    //                } else {
    //                    DestinoNo = $($radioPontosDeInteresse.selector + ':checked').val()
    //                    $($radioPontosDeInteresse.selector + ":checked").each(function () {
    //                        var idVal = $(this).attr("id");
    //                        NomeDestino = ($("label[for='" + idVal + "']").text());
    //                    });
    //                };

    //                montarBuscarLocal(OrigemNo, DestinoNo, NomeOrigem, NomeDestino);
    //            } else {
    //                $($btnContinuarCruzamentoLocal).trigger('click');
    //            };
    //        };

    //    }).catch(function (ex) {
    //        terminaLoading();
    //        $("#divFormBuscaLocal").show();
    //        exibirMensagemErro('Ocorreu um erro, por favor tente novamente.');
    //        console.error('ERRO promisses: ' + ex);
    //    });

    //});

    $($btnBuscarLocal).on('click', function () {

        esconderDivs();

        var reqOrigem, NomeOrigem, NomeDestino;
        var OrigemNo = 0;
        var DestinoNo = 0;

        $("#btnContinuarBuscarLinha").show();

        $("#divFormBuscaLocal").hide();

        //#region pegaValores

        var reqEndereco, OrigemNo; //, NomeOrigem;
                
        if (!$("#txtbuscaLocalLinha").val().trim()) {
            exibirMensagemErro('Por favor, preencha os campos de "Local"');
            $("#divFormBuscaLocal").show();
            return;
        }        
        
        var numero = $("#txtbuscaLocalLinhaNumeroInicio").val().trim();
        var numeroFim = $("#txtbuscaLocalLinhaNumeroFim").val().trim();
        
        if(!numeroFim)
        numero = "0";

        if (!numero)
            numero = numeroFim;

        reqEndereco = buscarEndereco($("#txtbuscaLocalLinha").val(), numero ? numero : "0");
                
        //#endregion chamadas Destino

        Promise.all([reqEndereco]).then(function () {

            terminaLoading();

            var respostaOrigem;            

            respostaOrigem = reqEndereco.responseJSON;
            if (respostaOrigem) {

                if (reqEndereco.responseJSON.codigoErro) {
                    console.error('Resposta BuscarEndereco erro. Código: ' + reqEndereco.responseJSON.codigoErro + '. Mensagem: ' + reqEndereco.responseJSON.mensagem);
                    $("#divSelecaoEnderecosBuscaLinha").show('fast',function(){
                        $("#divSelecaoEnderecosBuscaLinha .filtros-busca-itinerarios").hide();
                    });
                    $("#pTextoResultadosLinha").text('');
                    $('label[for="divOptionsOrigemLinha"').hide();
                    $("#divOptionsOrigemLinha").hide();
                    $("#btnContinuarBuscarLinha").hide();
                    exibirMensagemErro(reqEndereco.responseJSON.mensagem);

                } else if (respostaOrigem.length > 1) {

                    $("#divSelecaoEnderecosBuscaLinha").show();
                    $("#pTextoResultadosLinha").text('Foram encontrados vários resultados para a sua busca. Por favor, selecione abaixo o resultado desejado e clique em "Continuar".');
                    $("#btnContinuarBuscarLinha").show();

                    populaDivOptionsSubSelecao($("#divOptionsOrigemLinha"), respostaOrigem, true, false, false, true, (numero != ""), (numeroFim != ""));

                } else if (respostaOrigem.length == 1) {

                    OrigemNo = respostaOrigem[0].identificadorNo;
                    //NomeOrigem = respostaOrigem[0].nomeRua + " " + respostaOrigem[0].numeroInicial + " a " + respostaOrigem[0].numeroFinal + ", " + respostaOrigem[0].bairro + ", " + respostaOrigem[0].cep + ' ';
                    populaDivOptionsSubSelecao($("#divOptionsOrigemLinha"), respostaOrigem, true, false, false, true, (numero != ""), (numeroFim != ""));
                };
            };

            if (OrigemNo && OrigemNo != 0) {
                montarBuscarLinha();
            };

        }).catch(function (ex) {
            terminaLoading();
            $("#divFormBuscaLocal").show();
            exibirMensagemErro('Ocorreu um erro, por favor tente novamente.');
            console.error('ERRO promisses: ' + ex);
        });

    });

    $($btnContinuarBuscarLocal).on('click', function () {

        OrigemNo = Number($("input[name='grupoRadioOrigem']:checked").val());
        NomeOrigem = $("input[name='grupoRadioOrigem']:checked").attr('datanome');

        if ($($radioPontosDeInteresse.selector + ':checked').val() == 'O') {
            DestinoNo = $($dropdownPontoItinerarioDestinoLocal).val();
            NomeDestino = $($dropdownPontoItinerarioDestinoLocal.selector + ' option:selected').text();
        } else {
            DestinoNo = $($radioPontosDeInteresse.selector + ':checked').val()
            $($radioPontosDeInteresse.selector + ":checked").each(function () {
                var idVal = $(this).attr("id");
                NomeDestino = ($("label[for='" + idVal + "']").text());
            });
        };

        montarBuscarLocal(OrigemNo, DestinoNo, NomeOrigem, NomeDestino);

    });

    $($btnContinuarCruzamentoLocal).on('click', function () {

        $($btnContinuarCruzamentoLocal).hide();
        $($btnContinuarBuscarLocal).show();
        $("#divFormBuscaLocal").hide();
        $("#divSelecaoEnderecosLocal").hide();

        var reqOrigemCep, NomeOrigem, NomeDestino;
        var OrigemNo = 0;
        var DestinoNo = 0;

        var OrigemIBGE = $("input[name='grupoRadioDestino']:checked").val();

        var txtCruzamentoFinaloOrigem = $($txtCruzamentoFinaloOrigemLocal).val();

        var selecaoPontoOrigem = $($dropdownPontoItinerarioOrigemLocal).val();
        if (selecaoPontoOrigem == "s_02") {
            reqOrigemCep = buscarCruzamento(OrigemIBGE, txtCruzamentoFinaloOrigem);
        } else {
            reqOrigemCep = new Promise(function (res, rej) { res(""); });
            if (selecaoPontoOrigem == "s_01") {

                var valorSelecionado = Number($("input[name='grupoRadioOrigem']:checked").val());
                $divOptionsOrigemLocal.find('.form-check [value!="' + valorSelecionado + '"][for!="rdOr' + valorSelecionado + '"]').remove().end();
                OrigemNo = valorSelecionado;
                NomeOrigem = $("input[name='grupoRadioOrigem']:checked").attr('datanome');

            } else {
                var selecaoSubPontoOrigem = $($dropdownPontoItinerarioOrigemSubSelecaoLocal).val();
                reqOrigemCep = verificarGfNosID(selecaoSubPontoOrigem, selecaoPontoOrigem, 1);
            };
        };

        Promise.all([reqOrigemCep]).then(function () {

            terminaLoading();

            if (reqOrigemCep && reqOrigemCep.responseJSON && reqOrigemCep.responseJSON.codigoErro) {
                console.error('Resposta BuscarEndereco erro. Código: ' + reqOrigemCep.responseJSON.codigoErro + '. Mensagem: ' + reqOrigemCep.responseJSON.mensagem);
                $("#divSelecaoEnderecosLocal").show();
                $("#pTextoResultadosLocal").text('');
                $('label[for="divOptionsOrigemLocal"').hide();
                $($divOptionsOrigemLocal).hide();
                $($btnContinuarCruzamentoLocal).hide();
                $($btnContinuarBuscarLocal).hide();
                exibirMensagemErro(reqOrigemCep.responseJSON.mensagem);
            } else {

                var respostaOrigem = reqOrigemCep.responseJSON;

                if (reqOrigemCep.responseJSON && (reqOrigemCep.responseJSON.length == 1)) {

                    OrigemNo = reqOrigemCep.responseJSON[0].identificadorNo
                    NomeOrigem = respostaOrigem[0].nomeRua + " " + respostaOrigem[0].numeroInicial + " a " + respostaOrigem[0].numeroFinal + ", " + respostaOrigem[0].bairro + ", " + respostaOrigem[0].cep + ' ';

                } else {

                    if (reqOrigemCep.responseJSON) {
                        if (reqOrigemCep.responseJSON.length > 1) {

                            $("#divFormBuscaLocal").hide();
                            $("#divSelecaoEnderecosLocal").show();
                            $("#pTextoResultadosLocal").text('Foram encontrados diversos cruzamentos para a sua busca. Por favor, selecione abaixo o desejado e clique em "Continuar".');

                            populaDivOptionsSubSelecao($divOptionsOrigemLocal, reqOrigemCep.responseJSON, true, false, false);

                        } else if (reqOrigemCep.responseJSON.length == 1) {
                            OrigemNo = reqOrigemCep.responseJSON[0].identificadorNo
                            NomeOrigem = reqOrigemCep.responseJSON[0].nomeRua + " " + reqOrigemCep.responseJSON[0].numeroInicial + " a " + reqOrigemCep.responseJSON[0].numeroFinal + ", " + reqOrigemCep.responseJSON[0].bairro + ", " + reqOrigemCep.responseJSON[0].cep + ' ';
                            populaDivOptionsSubSelecao($divOptionsOrigemLocal, reqOrigemCep.responseJSON, true, false, false);
                        } else {
                            OrigemNo = reqOrigemCep.responseJSON;
                            NomeOrigem = $($dropdownPontoItinerarioOrigemSubSelecaoLocal).children("option").filter(":selected").text();
                        };
                    };

                };

                if (OrigemNo != 0) {

                    if ($($radioPontosDeInteresse.selector + ':checked').val() == 'O') {
                        DestinoNo = $($dropdownPontoItinerarioDestinoLocal).val();
                        NomeDestino = $($dropdownPontoItinerarioDestinoLocal.selector + ' option:selected').text();
                    } else {
                        DestinoNo = $($radioPontosDeInteresse.selector + ':checked').val()
                        $($radioPontosDeInteresse.selector + ":checked").each(function () {
                            var idVal = $(this).attr("id");
                            NomeDestino = ($("label[for='" + idVal + "']").text());
                        });
                    };

                    montarBuscarLocal(OrigemNo, DestinoNo, NomeOrigem, NomeDestino);
                };

            };
        }).catch(function () {
            terminaLoading();
            $("#divFormBuscaLocal").show();
            exibirMensagemErro('Ocorreu um erro, por favor tente novamente.');
            console.error('ERRO promisses: ' + ex);
        });

    });

    $($btnVoltarBuscarLocal).on('click', function () {
        $("#divFormBuscaLocal").show();
        $("#divSelecaoEnderecosLocal").hide();
        esconderDivs();
    });

    $($btnBuscarItinerarioPorLinha).on('click', function () {

        var reqEndereco, OrigemNo, NomeOrigem;

        $("#divFormBuscaLinha").hide();
        
        //if (!$("#autocomplete-overlay").val() && !$("#txtbuscaLocalLinha").val()) {
        //    exibirMensagemErro('Por favor, preencha os campos "Linha" e/ou "Local"');
        //    $("#divFormBuscaLinha").show();
        //    return;
        //}

        if (!$("#autocomplete-overlay").val().trim()) {
            exibirMensagemErro('Por favor, digite o número ou o nome da linha');
            $("#divFormBuscaLinha").show();
            return;
        }

        //if ($("#txtbuscaLocalLinha").val() && $("#txtbuscaLocalLinha").val() != '') {
        //    var numero = $("#txtbuscaLocalLinhaNumeroInicio").val();

        //    reqEndereco = buscarEndereco($("#txtbuscaLocalLinha").val(), numero ? numero : "0");
        //} else {
        //    reqEndereco = new Promise(function (res, rej) { res(""); });
        //}
        
        reqEndereco = new Promise(function (res, rej) { res(""); });        

        Promise.all([reqEndereco]).then(function () {

            terminaLoading();            

            var respostaOrigem;

            if (!reqEndereco.responseJSON) {
                montarBuscarLinha();
            }

            //else {

            //    respostaOrigem = reqEndereco.responseJSON;
            //    if (respostaOrigem) {

            //        if (reqEndereco.responseJSON.codigoErro) {
            //            console.error('Resposta BuscarEndereco erro. Código: ' + reqEndereco.responseJSON.codigoErro + '. Mensagem: ' + reqEndereco.responseJSON.mensagem);
            //            $("#divSelecaoEnderecosBuscaLinha").show();
            //            $("#pTextoResultadosLinha").text('');
            //            $('label[for="divOptionsOrigemLinha"').hide();
            //            $("#divOptionsOrigemLinha").hide();
            //            $("#btnContinuarBuscarLinha").hide();
            //            exibirMensagemErro(reqEndereco.responseJSON.mensagem);

            //        } else if (respostaOrigem.length > 1) {

            //            $("#divSelecaoEnderecosBuscaLinha").show();
            //            $("#pTextoResultadosLinha").text('Foram encontrados vários resultados para a sua busca. Por favor, selecione abaixo o resultado desejado e clique em "Continuar".');
            //            $("#btnContinuarBuscarLinha").show();

            //            populaDivOptionsSubSelecao($("#divOptionsOrigemLinha"), respostaOrigem, true, false, false, true);

            //        } else if (respostaOrigem.length == 1) {

            //            OrigemNo = respostaOrigem[0].identificadorNo;
            //            NomeOrigem = respostaOrigem[0].nomeRua + " " + respostaOrigem[0].numeroInicial + " a " + respostaOrigem[0].numeroFinal + ", " + respostaOrigem[0].bairro + ", " + respostaOrigem[0].cep + ' ';
            //            populaDivOptionsSubSelecao($("#divOptionsOrigemLinha"), respostaOrigem, true, false, false, true);
            //        };
            //    };

            //    if (OrigemNo && OrigemNo != 0) {
            //        montarBuscarLinha();
            //    };
            //}
        }).catch(function (ex) {
            terminaLoading();
            $("#divFormBuscaLinha").show();
            exibirMensagemErro('Ocorreu um erro, por favor tente novamente.');
            console.error('ERRO promisses: ' + ex);
        });
    });

    $("#btnVoltarBuscarLinha").on('click', function () {
        $("#divSelecaoEnderecosBuscaLinha").hide();
        $("#divFormBuscaLocal").show();
        esconderDivs();
    });

    $("#btnContinuarBuscarLinha").on('click', function () {
        montarBuscarLinha();
    });

    $("[data-toggle='tooltip']").tooltip({        
        html: true
    });
});


function populaDivOptionsSubSelecao(div, list, origem, ibge, selecao, buscaLinha, temNumInicial, temNumFinal) {

    temNumInicial = ((temNumInicial != undefined) ? temNumInicial: true);
    temNumFinal = ((temNumFinal != undefined) ? temNumFinal : true);

    var OrDs = 'Ds';
    var OrigemDestino = 'Destino';

    if (origem) {
        OrDs = 'Or';
        OrigemDestino = 'Origem';
    };

    if (buscaLinha) {
        OrigemDestino += 'BuscaLinha';
    }

    var length = list.length;
    div.find('.form-check').remove().end();
    $(div).show();
    var labelId = $(div).prop('id');
    $('label[for="'+labelId+'"]').show();

    for (var j = 0; j < length; j++) {

        var item = list[j];
        var nome = '';
        var numI = item.numeroInicial;
        var numF = item.numeroFinal;
        if (selecao) {
            nome = item.nome;
        } else {
            nome = item.nomeRua;

            if (temNumInicial || temNumFinal) {
                nome += " " + numI + " a " + numF;
            }
            else {
                numI = 0;
                numF = 0;
            }

            if (item.bairro) {
                nome += ", " + item.bairro;
            }

            if (item.cep) {
                nome += ", " + item.cep + ' ';
            }
        }

        var valor = item.identificadorNo;
        if (ibge) {
            valor = item.codigoVia;
        }

        div.append(
        '<div class="form-check" style="display:block;">' +
        '<input class="form-check-input" style="float:left;" type="radio" dataTreNumI="' + numI + '" ' + 
            'dataTreNumF="' + numF + '" datalat="' + item.latitude + '" datalong="' + item.longitude + '" ' + 
            'datagfTreID="' + item.identificadorTrecho + '" dataIbge="' + item.codigoVia + '" datacodLog="' + item.codigoLogradouro + '" ' + 
            'name="grupoRadio' + OrigemDestino + '" datanome="' + nome + '" id="rd' + OrDs + item.identificadorNo + '" ' + 
            'value="' + valor + '" ' + (j == 0 ? 'checked=checked' : '') + ' >' +
        '<label class="form-check-label" style="padding-left:0.4em;width:90%" for="rd' + OrDs + item.identificadorNo + '">' +
        ' ' + nome +
        '</label>' +
        '</div>'
        );
    };
};
function popularForm() {
    if (window.paramTrajeto) {

        $($txtEnderecoOrigem).val(window.paramTrajeto.txtEnderecoOrigem);
        $($txtNumeroEnderecoOrigem).val(window.paramTrajeto.txtNumeroEnderecoOrigem);
        $($txtCruzamentoInicioOrigem).val(window.paramTrajeto.txtCruzamentoInicioOrigem);
        $($txtCruzamentoFinaloOrigem).val(window.paramTrajeto.txtCruzamentoFinaloOrigem);
        $($txtEnderecoDestino).val(window.paramTrajeto.txtEnderecoDestino);
        $($txtNumeroEnderecoDestino).val(window.paramTrajeto.txtNumeroEnderecoDestino);
        $($txtCruzamentoInicioDestino).val(window.paramTrajeto.txtCruzamentoInicioDestino);
        $($txtCruzamentoFinaloDestino).val(window.paramTrajeto.txtCruzamentoFinaloDestino);

        //$($chkMetro)[0].checked = window.paramTrajeto.descMetro;
        //$($chkCPTM)[0].checked = window.paramTrajeto.descCPTM;

        //$($chkLinhasAcessiveis)[0].checked = window.paramTrajeto.ppd;
        //$($selectFaixaHoraria).val((window.paramTrajeto.horario ? window.paramTrajeto.horario : (new Date().getHours())));
        //$($selectDiaUtil).val(window.paramTrajeto.tipoDia);
        //$($selectPrioridade).val((window.paramTrajeto.otimizacao ? window.paramTrajeto.otimizacao : "T"));
        //$($txtQueroAndar).val((window.paramTrajeto.maxPe ? window.paramTrajeto.maxPe : 600));


        if (window.paramTrajeto.selecaoPontoOrigem) {
            $($chkMetro)[0].checked = (Number(window.paramTrajeto.dM) ? 0 : 1);
            $($chkCPTM)[0].checked = (Number(window.paramTrajeto.dC) ? 0 : 1);
            $($selectDiaUtil).val(window.paramTrajeto.tD);
        }
        else {
            $($chkMetro)[0].checked = 0;
            $($chkCPTM)[0].checked = 0;

            var day = (new Date().getDay());
            if (day == 0) {
                document.getElementById("selectDiaUtil").selectedIndex = 2;
            } else if (day == 6) {
                document.getElementById("selectDiaUtil").selectedIndex = 1;
            } else {
                document.getElementById("selectDiaUtil").selectedIndex = 0;
            };
        }
        
        //$($chkLinhasAcessiveis)[0].checked = Number(window.paramTrajeto.p);        
        $($selectFaixaHoraria).val((window.paramTrajeto.h ? window.paramTrajeto.h : (new Date().getHours())));                      
        $($selectPrioridade).val((window.paramTrajeto.o ? window.paramTrajeto.o : "T"));        
        $($txtQueroAndar).val((window.paramTrajeto.mP ? window.paramTrajeto.mP : 600));

        //if (window.paramTrajeto.selecaoPontoOrigem) {
        //    $($dropdownPontoItinerarioOrigem).val(window.paramTrajeto.selecaoPontoOrigem);
        //    $($dropdownPontoItinerarioOrigem).trigger('change');
        //};
        //if (window.paramTrajeto.selecaoPontoDestino) {
        //    $($dropdownPontoItinerarioDestino).val(window.paramTrajeto.selecaoPontoDestino);
        //    $($dropdownPontoItinerarioDestino).trigger('change');
        //};

        //$($dropdownPontoItinerarioOrigemSubSelecao).val(window.paramTrajeto.selecaoSubPontoOrigem);
        //$($dropdownPontoItinerarioDestinoSubSelecao).val(window.paramTrajeto.selecaoSubPontoDestino);

        //$("#autocomplete-overlay").val(window.paramTrajeto.linha);
        //$("#txtbuscaLocalLinha").val(window.paramTrajeto.local);
        //$("#txtbuscaLocalLinhaNumeroInicio").val(window.paramTrajeto.localNumeroInicio);
        //$("#txtbuscaLocalLinhaNumeroFim").val(window.paramTrajeto.localNumeroFim);
        //$("#chkLinhasAcessiveisLinhas")[0].checked = window.paramTrajeto.ppdLinha;
        //$("#chkLinhasNoturnasLinhas")[0].checked = window.paramTrajeto.noturnaLinha;
        //$("#selectDiaUtilLinha").val(window.paramTrajeto.tipoDiaLinha);

        //if (!window.paramTrajeto.tipoDiaLinha) {
        //    var day = (new Date().getDay());
        //    if (day == 0) {
        //        document.getElementById("selectDiaUtilLinha").selectedIndex = 2;
        //    } else if (day == 6) {
        //        document.getElementById("selectDiaUtilLinha").selectedIndex = 1;
        //    } else {
        //        document.getElementById("selectDiaUtilLinha").selectedIndex = 0;
        //    };
        //};
                
        //$linhaSelecionada = window.paramTrajeto.li;        

        $("#txtbuscaLocalLinha").val(window.paramTrajeto.lo);
        $("#txtbuscaLocalLinhaNumeroInicio").val(window.paramTrajeto.lNI);
        $("#txtbuscaLocalLinhaNumeroFim").val(window.paramTrajeto.lNF);
        //$("#chkLinhasAcessiveisLinhas")[0].checked = window.paramTrajeto.pL;
        $("#chkLinhasNoturnasLinhas")[0].checked = window.paramTrajeto.nL;
        $("#selectDiaUtilLinha").val(window.paramTrajeto.tDL);

        if (!window.paramTrajeto.tDL) {
            var day = (new Date().getDay());
            if (day == 0) {
                document.getElementById("selectDiaUtilLinha").selectedIndex = 2;
            } else if (day == 6) {
                document.getElementById("selectDiaUtilLinha").selectedIndex = 1;
            } else {
                document.getElementById("selectDiaUtilLinha").selectedIndex = 0;
            };
        };

        $($radioPontosDeInteresse.selector + '[value="' + window.paramTrajeto.radioPontosDeInteresse + '"]').prop("checked", true);

        if (window.paramTrajeto.dropdownPontoItinerarioDestinoLocal) {
            $($dropdownPontoItinerarioDestinoLocal).val(window.paramTrajeto.dropdownPontoItinerarioDestinoLocal);
        };

        if (window.paramTrajeto.dropdownPontoItinerarioOrigemLocal) {
            $($dropdownPontoItinerarioOrigemLocal).val(window.paramTrajeto.dropdownPontoItinerarioOrigemLocal);
            $($dropdownPontoItinerarioOrigemLocal).trigger('change');
        };
        $($txtEnderecoOrigemLocal).val(window.paramTrajeto.txtEnderecoOrigemLocal);
        $($txtNumeroEnderecoOrigemLocal).val(window.paramTrajeto.txtNumeroEnderecoOrigemLocal);
        $($txtCruzamentoInicioOrigemLocal).val(window.paramTrajeto.txtCruzamentoInicioOrigemLocal);
        $($txtCruzamentoFinaloOrigemLocal).val(window.paramTrajeto.txtCruzamentoFinaloOrigemLocal);
        $($dropdownPontoItinerarioOrigemSubSelecaoLocal).val(window.paramTrajeto.dropdownPontoItinerarioOrigemSubSelecaoLocal);


    } else {

        $($selectFaixaHoraria).val((new Date().getHours()));

        var day = (new Date().getDay());
        if (day == 0) {
            document.getElementById("selectDiaUtil").selectedIndex = 2;
        } else if (day == 6) {
            document.getElementById("selectDiaUtil").selectedIndex = 1;
        } else {
            document.getElementById("selectDiaUtil").selectedIndex = 0;
        };
    };
};


function inputValueTemplate(result) {
    return result && result.letreiro;
}

function buscarLinhas() {

    var urlApi = urlApiInfotrans + "RetornarLinhas";

    var ajax = $.ajax({
        url: urlApi,
        type: 'POST',
        contentType: 'application/json',
        dataType: "json",
        success: function (response) {
            if (response.length && response.length > 0) { 

                window.TodasLinhas = response;

                response = response.filter(objeto => {
                    // return !objeto.letreiro.includes("-1 ") && !objeto.letreiro.includes("8700-24") && !objeto.letreiro.includes("METRÔ L") && !objeto.letreiro.includes("CPTM L");
                    return !objeto.letreiro.includes("METRÔ L") && !objeto.letreiro.includes("CPTM L"); 
                });

                element = document.querySelector('#tt-overlay')
                id = 'autocomplete-overlay'
                accessibleAutocomplete({
                    displayMenu: 'overlay',
                    tNoResults: function () { return 'Linha não encontrada' },
                    placeholder: 'Exemplo: 8200-10',
                    minLength: 2,
                    element: element,
                    //defaultValue: (($linhaSelecionada) ? $linhaSelecionada : ""),
                    id: id,
                    source: function (q, s) {
                        s(q ? 
                            response.filter(function(r) {
                                r = RemoveAccents(r.letreiro);
                                q = RemoveAccents(q);                                
                                return r.indexOf(q.toUpperCase()) !== -1;
                            })
                        : [])
                    },
                    templates: {
                        inputValue: inputValueTemplate,
                        suggestion: inputValueTemplate
                    },
                    onConfirm: function (val) {
                        if (val && val != "" && val != undefined) {
                            redirecionarDetalheLinha(val.letreiro, val.CdPjOID);
                        }
                    }
                });
            } else {
                console.error('Erro API buscarLinhas: resposta vazia');
            };
        },
        error: function (e) { console.error('Erro API buscarLinhas', e) }
    });
};

function redirecionarDetalheLinha(letreiro, cdPjOID) {
    window.location.href = "/itinerarios/linha/?numero="+letreiro.substring(0, 7);
}

function buscarPontosDefinidos() {

    var urlApi = urlApiInfotrans + "BuscarPontosDefinidos";

    var ajax = $.ajax({
        url: urlApi,
        type: 'POST',
        crossDomain: true,
        contentType: 'application/json',
        dataType: "json",
        success: function (response) {
            if (response.length && response.length > 0) {
                for (var i = 0; i < response.length; i++) {
                    var cod = response[i].cod;
                    var nome = response[i].nome;
                    var pontos = response[i].pontos;
                    listPontosDefinidos[cod] = { "nome": nome, "pontos": pontos };
                    //$dropdownPontoItinerarioOrigem.append($("<option />").val(cod).text(nome));
                    //$dropdownPontoItinerarioDestino.append($("<option />").val(cod).text(nome));
                    $dropdownPontoItinerarioOrigemLocal.append($("<option />").val(cod).text(nome));
                    $dropdownPontoItinerarioDestinoLocal.append($("<option />").val(cod).text(nome));
                };

                popularForm();

            } else {
                console.error('Erro API PontosDefinidos: resposta vazia');
            };
        },
        error: function () { console.error('Erro API PontosDefinidos') }
    });
};
function verificarGfNosID(cod_ponto, cod_grupo) {

    var urlApi = urlApiInfotrans + "VerificarGfNosID";
    var json = { "cdNotID": cod_ponto, "tpNotID": cod_grupo };

    var ajax = $.ajax({
        url: urlApi,
        type: 'POST',
        beforeSend: function () { comecaLoading(); },
        crossDomain: true,
        contentType: 'application/json',
        dataType: "json",
        data: JSON.stringify(json),
        success: function (response) {
            if (!response) {
                console.error('Erro API verificarGfNosID: resposta vazia');
            };
        },
        error: function () { console.error('Erro API verificarGfNosID') }
    });

    return ajax;
};
function buscarEndereco(end, num) {
    var urlApi = urlApiInfotrans + "BuscarEndereco";
    var json = { "end": end, "num": num };

    var ajax = $.ajax({
        url: urlApi,
        type: 'POST',
        crossDomain: true,
        beforeSend: function () { comecaLoading(); },
        //complete: function () { terminaLoading(); },
        contentType: 'application/json',
        dataType: "json",
        data: JSON.stringify(json),
        success: function (response) {
            if (!response) {
                console.error('Erro API buscarEndereco: resposta vazia');
            };
        },
        error: function () { console.error('Erro API buscarEndereco') }
    });

    return ajax;
};
function buscarCruzamento(codEnd1, end2) {
    var urlApi = urlApiInfotrans + "BuscarCruzamento";
    var json = { "codEnd1": codEnd1, "end2": end2 };

    var ajax = $.ajax({
        url: urlApi,
        type: 'POST',
        beforeSend: function () { comecaLoading(); },
        //complete: function () { terminaLoading(); },
        crossDomain: true,
        contentType: 'application/json',
        dataType: "json",
        data: JSON.stringify(json),
        success: function (response) {
            if (!response) {
                console.error('Erro API buscarEndereco: resposta vazia');
            };
        },
        error: function () { console.error('Erro API buscarEndereco') }
    });

    return ajax;
};

function montarTrajeto(codOrigem, codDestino, NomeOrigem, NomeDestino) {

    var descMetro = ($($chkMetro)[0].checked ? 0 : 1);
    var descCPTM = ($($chkCPTM)[0].checked ? 0 : 1);
    var ppd = 0; //($($chkLinhasAcessiveis)[0].checked ? 1 : 0);
    var horario = Number($($selectFaixaHoraria).val());
    var tipoDia = Number($($selectDiaUtil).val());
    var otimizacao = $($selectPrioridade).val();
    var maxPe = Number($($txtQueroAndar).val());
    //var selecaoPontoOrigem = $($dropdownPontoItinerarioOrigem).val();
    var selecaoPontoOrigem = "s_01";
    var txtEnderecoOrigem = $($txtEnderecoOrigem).val();
    var txtNumeroEnderecoOrigem = $($txtNumeroEnderecoOrigem).val();
    var txtCruzamentoInicioOrigem = $($txtCruzamentoInicioOrigem).val();
    var txtCruzamentoFinaloOrigem = $($txtCruzamentoFinaloOrigem).val();
    //var selecaoPontoDestino = $($dropdownPontoItinerarioDestino).val();
    var selecaoPontoDestino = "s_01";
    var txtEnderecoDestino = $($txtEnderecoDestino).val();
    var txtNumeroEnderecoDestino = $($txtNumeroEnderecoDestino).val();
    var txtCruzamentoInicioDestino = $($txtCruzamentoInicioDestino).val();
    var txtCruzamentoFinaloDestino = $($txtCruzamentoFinaloDestino).val();
    //var selecaoSubPontoOrigem = $($dropdownPontoItinerarioOrigemSubSelecao).val();
    //var selecaoSubPontoDestino = $($dropdownPontoItinerarioDestinoSubSelecao).val();
    var selecaoSubPontoOrigem = null;
    var selecaoSubPontoDestino = null;

    /*********************************************************
    30/11   - Anderson - Alterada lógica dos checks de metrô e CPTM;
                       - Removido campos de trajeto que não serão mais usados, porém lógica dos checks parou de funcionar. Verificar.
    **********************************************************/


    var jsonQuery = {
        "m": "mtrTrj",
        "codOrigem": codOrigem, "codDestino": codDestino, "descMetro": descMetro, "descCPTM": descCPTM,
        "maxPe": maxPe, "tipoDia": tipoDia, "horario": horario, "ppd": ppd, "otimizacao": otimizacao,
        "nomeOrigem": NomeOrigem, "nomeDestino": NomeDestino, "selecaoPontoOrigem": selecaoPontoOrigem,
        "txtEnderecoOrigem": txtEnderecoOrigem, "txtNumeroEnderecoOrigem": txtNumeroEnderecoOrigem,
        "txtCruzamentoInicioOrigem": txtCruzamentoInicioOrigem, "txtCruzamentoFinaloOrigem": txtCruzamentoFinaloOrigem,
        "selecaoPontoDestino": selecaoPontoDestino, "txtEnderecoDestino": txtEnderecoDestino, "txtNumeroEnderecoDestino": txtNumeroEnderecoDestino,
        "txtCruzamentoInicioDestino": txtCruzamentoInicioDestino, "txtCruzamentoFinaloDestino": txtCruzamentoFinaloDestino, "selecaoSubPontoOrigem": selecaoSubPontoOrigem,
        "selecaoSubPontoDestino": selecaoSubPontoDestino
    };

    var url = '/itinerarios/trajeto/trecho';

    var form = document.createElement('form');
    form.style.visibility = 'hidden'; // no user interaction is necessary
    form.method = 'POST'; // forms by default use GET query strings
    form.action = url;
    for (key in jsonQuery) {
        var input = document.createElement('input');
        input.name = key;
        input.value = jsonQuery[key];
        form.appendChild(input); // add key/value pair to form
    }
    document.body.appendChild(form); // forms cannot be submitted outside of body
    form.submit();
};
function montarBuscarLinha() {

    var id_local = Number($("input[name='grupoRadioOrigemBuscaLinha']:checked").val());
    var gf_treid = Number($("input[name='grupoRadioOrigemBuscaLinha']:checked").attr('datagfTreID'));
    var cod_ibge = Number($("input[name='grupoRadioOrigemBuscaLinha']:checked").attr('dataIbge'));
    var cod_log = Number($("input[name='grupoRadioOrigemBuscaLinha']:checked").attr('datacodLog'));
    var NomeOrigem = $("input[name='grupoRadioOrigemBuscaLinha']:checked").attr('datanome');
    var lat = $("input[name='grupoRadioOrigemBuscaLinha']:checked").attr('datalat');
    var long = $("input[name='grupoRadioOrigemBuscaLinha']:checked").attr('datalong');
    var treNumI = Number($("input[name='grupoRadioOrigemBuscaLinha']:checked").attr('dataTreNumI'));
    var treNumF = Number($("input[name='grupoRadioOrigemBuscaLinha']:checked").attr('dataTreNumF'));

    var linha = $("#autocomplete-overlay").val();
    var local = $("#txtbuscaLocalLinha").val();
    var localNumeroInicio = $("#txtbuscaLocalLinhaNumeroInicio").val().trim();

    if (!localNumeroInicio && treNumI) {
        localNumeroInicio = treNumI;
    }

    var localNumeroFim = $("#txtbuscaLocalLinhaNumeroFim").val().trim();

    if (!localNumeroFim && treNumF) {
        localNumeroFim = treNumF;
    }
    var idLocal = id_local ? id_local : 0;
    var gfTreID = gf_treid ? gf_treid : 0;
    var codIbge = cod_ibge ? cod_ibge : 0;
    var codLog = cod_log ? cod_log : 0;
    var ppdLinha = 0;//($("#chkLinhasAcessiveisLinhas")[0].checked ? 1 : 0);
    var noturnaLinha = ($("#chkLinhasNoturnasLinhas")[0].checked ? 1 : 0);
    var tipoDiaLinha = Number($("#selectDiaUtilLinha").val());

    var jsonQuery = {
        "m": "bscLin",
        "linha": linha,
        "local": local,
        "localNumeroInicio": localNumeroInicio,
        "localNumeroFim": localNumeroFim,
        "idLocal": idLocal,
        "gfTreID": gfTreID,
        "codIbge": codIbge,
        "codLog" : codLog,
        "tipoDiaLinha": tipoDiaLinha,
        "ppdLinha": ppdLinha,
        "noturnaLinha": noturnaLinha,
        "nomeOrigem": NomeOrigem,
        "latitude": lat,
        "longitude": long
    };

    var url = '/itinerarios/trajeto/trecho';

    var form = document.createElement('form');
    form.style.visibility = 'hidden';
    form.method = 'POST';
    form.action = url;
    for (key in jsonQuery) {
        var input = document.createElement('input');
        input.name = key;
        input.value = jsonQuery[key];
        form.appendChild(input);
    }
    document.body.appendChild(form);
    form.submit();
};
function montarBuscarLocal(codOrigem, codDestino, NomeOrigem, NomeDestino) {

    var radioPontosDeInteresse = $($radioPontosDeInteresse.selector + ':checked').val();
    var dropdownPontoItinerarioDestinoLocal = $($dropdownPontoItinerarioDestinoLocal).val();
    var dropdownPontoItinerarioOrigemLocal = $($dropdownPontoItinerarioOrigemLocal).val();
    var txtEnderecoOrigemLocal = $($txtEnderecoOrigemLocal).val();
    var txtNumeroEnderecoOrigemLocal = $($txtNumeroEnderecoOrigemLocal).val();
    var txtCruzamentoInicioOrigemLocal = $($txtCruzamentoInicioOrigemLocal).val();
    var txtCruzamentoFinaloOrigemLocal = $($txtCruzamentoFinaloOrigemLocal).val();
    var dropdownPontoItinerarioOrigemSubSelecaoLocal = $($dropdownPontoItinerarioOrigemSubSelecaoLocal).val();



    var jsonQuery = {
        "m": "bscLoc",
        "v_numOpcoes": 5,
        "gfNosID": codOrigem,
        "tpNotID": codDestino,        
        "nomeOrigem": NomeOrigem,
        "nomeDestino": NomeDestino,
        "radioPontosDeInteresse": radioPontosDeInteresse,
        "dropdownPontoItinerarioDestinoLocal": dropdownPontoItinerarioDestinoLocal,
        "dropdownPontoItinerarioOrigemLocal": dropdownPontoItinerarioOrigemLocal,
        "txtEnderecoOrigemLocal": txtEnderecoOrigemLocal,
        "txtNumeroEnderecoOrigemLocal": txtNumeroEnderecoOrigemLocal,
        "txtCruzamentoInicioOrigemLocal": txtCruzamentoInicioOrigemLocal,
        "txtCruzamentoFinaloOrigemLocal": txtCruzamentoFinaloOrigemLocal,
        "dropdownPontoItinerarioOrigemSubSelecaoLocal": dropdownPontoItinerarioOrigemSubSelecaoLocal
    };

    var url = '/itinerarios/trajeto/trecho';

    var form = document.createElement('form');
    form.style.visibility = 'hidden'; // no user interaction is necessary
    form.method = 'POST'; // forms by default use GET query strings
    form.action = url;
    for (key in jsonQuery) {
        var input = document.createElement('input');
        input.name = key;
        input.value = jsonQuery[key];
        form.appendChild(input); // add key/value pair to form
    }
    document.body.appendChild(form); // forms cannot be submitted outside of body
    form.submit();
};