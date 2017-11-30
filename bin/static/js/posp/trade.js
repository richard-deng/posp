/**
 * Created by admin on 2017/11/26.
 */
$(document).ready(function () {

    var table = $('#tradeList').DataTable({
        "autoWidth": false,     //通常被禁用作为优化
        "processing": true,
        "serverSide": true,
        "paging": true,         //制指定它才能显示表格底部的分页按钮
        "info": true,
        "ordering": false,
        "searching": false,
        "lengthChange": true,
        "deferRender": true,
        "iDisplayLength": 10,
        "sPaginationType": "full_numbers",
        "lengthMenu": [[10, 40, 100],[10, 40, 100]],
        "dom": 'l<"top"p>rt',
        "fnInitComplete": function(){
            var $tradeList_length = $("#tradeList_length");
            var $tradeList_paginate = $("#tradeList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $tradeList_paginate.addClass('col-md-8');
            $tradeList_length.addClass('col-md-4');
            $tradeList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
                'page': Math.ceil(data.start / data.length) + 1,
                'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var syssn = $("#s_syssn").val();
            var userid = $("#s_userid").val();

            if(syssn){
                get_data.syssn = syssn;
            }

            if(userid){
                get_data.userid = userid;
            }

            var start_time = $("#start_time").val();
            var end_time = $("#end_time").val();
            if(start_time && end_time){
                var start_date = new Date(start_time);
                var end_date = new Date(end_time);
                if(end_date <= start_date){
                    toastr.warning('请核实时间范围');
                    return false;
                }
                get_data.start_time = start_time;
                get_data.end_time = end_time;
            }

            $.ajax({
                url: '/posp/v1/api/trade/list',
                type: 'GET',
                dataType: 'json',
                data: get_data,
                success: function(data) {
                    var respcd = data.respcd;
                    if(respcd !== '0000'){
                        $processing = $("#tradeList_processing");
                        $processing.css('display', 'none');
                        var resperr = data.resperr;
                        var respmsg = data.respmsg;
                        var msg = resperr ? resperr : respmsg;
                        toastr.warning(msg);
                        return false;
                    }
                    detail_data = data.data;
                    num = detail_data.num;
                    callback({
                        recordsTotal: num,
                        recordsFiltered: num,
                        data: detail_data.info
                    });
                },
                error: function(data) {
                    toastr.warning('获取数据异常');
                    return false;
                }
            });
        },
        'columnDefs': [
            {
                targets: 11,
                data: '操作',
                render: function(data, type, full) {
                    var syssn =full.syssn;
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-syssn="+syssn+">"+'查看'+"</button>";
                    return view;
                }
            }
        ],
        'columns': [
            { data: 'userid'},
            { data: 'chnlid'},
            { data: 'syssn'},
            { data: 'busicd'},
            { data: 'cardcd'},
            { data: 'retcd'},
            { data: 'cancel'},
            { data: 'txamt'},
            { data: 'sysdtm'},
            { data: 'origssn'},
            { data: 'servername'}
        ],
        'oLanguage': {
            'sProcessing': '<span style="color:red;">加载中....</span>',
            'sLengthMenu': '每页显示_MENU_条记录',
            'sInfo': '显示 _START_到_END_ 的 _TOTAL_条数据',
            'sInfoEmpty': '没有匹配的数据',
            'sZeroRecords': '没有找到匹配的数据',
            'oPaginate': {
                'sFirst': '首页',
                'sPrevious': '前一页',
                'sNext': '后一页',
                'sLast': '尾页'
            }
        }
    });

    $("#tradeSearch").click(function(){
        var trade_query_vt = $('#trade_query').validate({
           rules: {
               s_syssn: {
                   required: false,
                   maxlength: 60
               }
           },
           messages: {
               s_syssn: {
                   required: '请输入流水号',
                   maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
               }
           },
           errorPlacement: function(error, element){
               var $error_element = element.parent().parent().next();
               $error_element.text('');
               error.appendTo($error_element);
           }
        });
        var ok = trade_query_vt.form();
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1400);
            return false;
        }
        $('#tradeList').DataTable().draw();
    });

    $(document).on('click', '.viewEdit', function(){
        $("label.error").remove();
        $("#tradeViewForm").resetForm();
        var se_userid = window.localStorage.getItem('myid');
        var syssn = $(this).data('syssn');
        var get_data = {
            'se_userid': se_userid,
            'syssn': syssn
        };
        $.ajax({
            url: '/posp/v1/api/trade/view',
            type: 'GET',
            dataType: 'json',
            data: get_data,
            success: function(data) {
                var respcd = data.respcd;
                if(respcd !== '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                }
                else {
                    trade = data.data;
                    console.log(trade);
                    $('#cardcd_view').val(trade.cardcd);
                    $('#cardtp_view').val(trade.cardtp);
                    $('#chnlid_view').val(trade.chnlid);
                    $('#chnlsn_view').val(trade.chnlsn);
                    $('#issuerbank_view').val(trade.issuerbank);
                    $('#phonemodel_view').val(trade.phonemodel);
                    $('#psamid_view').val(trade.psamid);
                    $('#posentry_mode_view').val(trade.posentrymode);
                    $('#real_retcd_view').val(trade.real_retcd);
                    $('#terminal_id_view').val(trade.terminalid);

                    $('#tradeViewModal').modal();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });

});