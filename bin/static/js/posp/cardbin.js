$(document).ready(function(){

    var table = $('#cardBinList').DataTable({
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
            var $cardBinList_length = $("#cardBinList_length");
            var $cardBinList_paginate = $("#cardBinList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $cardBinList_paginate.addClass('col-md-8');
            $cardBinList_length.addClass('col-md-4');
            $cardBinList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var bank_name = $("#s_bank_name").val();

            if(bank_name){
                get_data.bankname = bank_name;
            }

            $.ajax({
	            url: '/posp/v1/api/card/list',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#cardBinList_processing");
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
                targets: 7,
                data: '操作',
                render: function(data, type, full) {
                    var card_bin_id =full.id;
                    var op = "<button type='button' class='btn btn-danger btn-sm delete' data-card_bin_id="+card_bin_id+">"+'删除'+"</button>";
                    var view ="<button type='button' class='btn btn-success btn-sm viewEdit' data-card_bin_id="+card_bin_id+">"+'查看'+"</button>";
                    return view+op;
                }
            }
        ],
		'columns': [
				{ data: 'bankname'},
                { data: 'bankid' },
				{ data: 'cardlen' },
				{ data: 'cardbin' },
				{ data: 'cardname' },
				{ data: 'cardtp' },
				{ data: 'foreign' },
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

    $("#cardBinSearch").click(function(){
        var card_bin_query_vt = $('#card_bin_query').validate({
           rules: {
               s_bank_name: {
                   required: false,
                   maxlength: 30
               },
           },
           messages: {
               s_bank_name: {
                   required: '请输入银行名称',
                   maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
               },
           },
           errorPlacement: function(error, element){
               var $error_element = element.parent().parent().next();
               $error_element.text('');
               error.appendTo($error_element);
           }
        });
        var ok = card_bin_query_vt.form();
        console.log('card_bin_query_vt status: ', ok);
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1000);
            return false;
        }
        $('#cardBinList').DataTable().draw();
    });

});