$(document).ready(function(){

    var table = $('#terminalList').DataTable({
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
            var $terminalList_length = $("#terminalList_length");
            var $terminalList_paginate = $("#terminalList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $terminalList_paginate.addClass('col-md-8');
            $terminalList_length.addClass('col-md-4');
            $terminalList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var terminal_id = $("#s_terminal_id").val();

            if(terminal_id){
                get_data.terminalid = terminal_id;
            }

            $.ajax({
	            url: '/posp/v1/api/terminal/list',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#terminalList_processing");
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
                targets: 8,
                data: '操作',
                render: function(data, type, full) {
                    var terminal_table_id =full.id;
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-terminal_table_id="+terminal_table_id+">"+'查看'+"</button>";
                    return view;
                }
            }
        ],
		'columns': [
				{ data: 'terminalid'},
                { data: 'psamid'},
				{ data: 'model'},
				{ data: 'deliver_date'},
				{ data: 'tck'},
				{ data: 'used'},
				{ data: 'state'},
				{ data: 'last_modify'},
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

    $("#terminalSearch").click(function(){
        var terminal_query_vt = $('#terminal_query').validate({
           rules: {
               s_terminal_id: {
                   required: false,
                   maxlength: 20
               }
           },
           messages: {
               s_terminal_id: {
                   required: '请输入通道ID',
                   maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
               }
           },
           errorPlacement: function(error, element){
               var $error_element = element.parent().parent().next();
               $error_element.text('');
               error.appendTo($error_element);
           }
        });
        var ok = terminal_query_vt.form();
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1000);
            return false;
        }
        $('#terminalList').DataTable().draw();
    });

	$("#terminalCreate").click(function(){
        $("#terminalCreateForm").resetForm();
        $("label.error").remove();
		$("#terminalCreateModal").modal();
	});

    $("#terminalCreateSubmit").click(function(){

        var terminal_create_vt = $('#terminalCreateForm').validate({
            rules: {

                produce_time_add: {
                    required: true,
                    maxlength: 20
                },
                deliver_time_add: {
                    required: true,
                    maxlength: 20
                },

                terminal_id_add: {
                    required: true,
                    maxlength: 20
                },

                psamid_add: {
                    required: true,
                    maxlength: 8
                },

                producer_add: {
                    required: true,
                    maxlength: 4
                },

                model_add: {
                    required: true,
                    maxlength: 4
                },

                tck_add: {
                    required: true,
                    maxlength: 32
                },

                advice_add: {
                    required: true,
                    maxlength: 256
                },

                qpos_pubkey_add: {
                    required: true,
                    maxlength: 256
                }

            },
            messages: {

                produce_time_add: {
                    required: '请选择生产日期',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                deliver_time_add: {
                    required: '请选择交付日期',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                terminal_id_add: {
                    required: '请输入终端ID',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                psamid_add: {
                    required: '请输入psamid',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                producer_add: {
                    required: '请输入生产商',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                model_add: {
                    required: '请输入模型',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                tck_add: {
                    required: '请输入tck',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                advice_add: {
                    required: '请输入advice',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                qpos_pubkey_add: {
                    required: '请输入公钥',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                }

            },
            errorPlacement: function(error, element){
                if(element.is(':checkbox')){
                    error.appendTo(element.parent().parent().parent());
                } else {
                    error.insertAfter(element);
                }
            }
        });

        var ok = terminal_create_vt.form();
        if(!ok){
            return false;
        }

        var post_data = {};
        var se_userid = window.localStorage.getItem('myid');

        post_data.se_userid = se_userid;
        post_data.produce_date = $('#produce_time_add').val();
        post_data.deliver_date = $('#deliver_time_add').val();
        post_data.terminalid = $('#terminal_id_add').val();
        post_data.psamid = $('#psamid_add').val();
        post_data.producer = $('#producer_add').val();
        post_data.model = $('#model_add').val();
        post_data.tck = $('#tck_add').val();
        post_data.advice = $('#advice_add').val();
        post_data.qpos_pubkey = $('#qpos_pubkey_add').val();
        post_data.used = $('#used_add').val();
        post_data.state = $('#state_add').val();

        $.ajax({
            url: '/posp/v1/api/terminal/create',
            type: 'POST',
            dataType: 'json',
            data: post_data,
            success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                    return false;
                }
                else {
                    toastr.success('添加终端成功');
                    $("#terminalCreateModal").modal('hide');
                    location.reload();
                    $('#terminalList').DataTable().draw();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });

    $(document).on('click', '.viewEdit', function(){
        $("label.error").remove();
        var se_userid = window.localStorage.getItem('myid');
        var terminal_table_id = $(this).data('terminal_table_id');
        $('#view_terminal_table_id').text(terminal_table_id);
        var get_data = {
            'se_userid': se_userid,
            'terminal_table_id': terminal_table_id
        };
        $.ajax({
            url: '/posp/v1/api/terminal/view',
            type: 'GET',
            dataType: 'json',
            data: get_data,
            success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                }
                else {
                    console.log(data.data);

                    var terminal = data.data;

                    $('input[name=produce_time_view]').val(terminal.produce_date);
                    $('input[name=deliver_time_view]').val(terminal.deliver_date);
                    $('#terminal_id_view').val(terminal.terminalid);
                    $('#psamid_view').val(terminal.psamid);
                    $('#producer_view').val(terminal.producer);
                    $('#model_view').val(terminal.model);
                    $('#tck_view').val(terminal.tck);
                    $('#advice_view').val(terminal.advice);
                    $('#used_view').val(terminal.used);
                    $('#state_view').val(terminal.state);
                    $('#qpos_pubkey_view').val(terminal.qpos_pubkey);

                    $('#datetimepicker3').datetimepicker('update');
                    $('#datetimepicker4').datetimepicker('update');

                    $("#terminalViewModal").modal();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });

    $('#terminalViewSubmit').click(function(){

        var terminal_edit_vt = $('#terminalViewForm').validate({
            rules: {
                produce_time_view: {
                    required: true,
                    maxlength: 20
                },
                deliver_time_view: {
                    required: true,
                    maxlength: 20
                },

                terminal_id_view: {
                    required: true,
                    maxlength: 20
                },

                psamid_view: {
                    required: true,
                    maxlength: 8
                },

                producer_view: {
                    required: true,
                    maxlength: 4
                },

                model_view: {
                    required: true,
                    maxlength: 4
                },

                tck_view: {
                    required: true,
                    maxlength: 32
                },

                advice_view: {
                    required: true,
                    maxlength: 256
                },

                qpos_pubkey_view: {
                    required: true,
                    maxlength: 256
                }

            },
            messages: {

                produce_time_view: {
                    required: '请选择生产日期',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                deliver_time_view: {
                    required: '请选择交付日期',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                terminal_id_view: {
                    required: '请输入终端ID',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                psamid_view: {
                    required: '请输入psamid',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                producer_view: {
                    required: '请输入生产商',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                model_view: {
                    required: '请输入模型',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                tck_view: {
                    required: '请输入tck',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                advice_view: {
                    required: '请输入advice',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                qpos_pubkey_view: {
                    required: '请输入公钥',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                }

            },
            errorPlacement: function(error, element){
                if(element.is(':checkbox')){
                    error.appendTo(element.parent().parent().parent());
                } else {
                    error.insertAfter(element);
                }
            }
        });
        var ok = terminal_edit_vt.form();
        if(!ok){
            return false;
        }

        var post_data = {};
        var terminal_table_id = $('#view_terminal_table_id').text();
        var se_userid = window.localStorage.getItem('myid');
        post_data['se_userid'] = se_userid;

        post_data.se_userid = se_userid;
        post_data.terminal_table_id = terminal_table_id;
        post_data.produce_date = $('#produce_time_view').val();
        post_data.deliver_date = $('#deliver_time_view').val();
        post_data.terminalid = $('#terminal_id_view').val();
        post_data.psamid = $('#psamid_view').val();
        post_data.producer = $('#producer_view').val();
        post_data.model = $('#model_view').val();
        post_data.tck = $('#tck_view').val();
        post_data.advice = $('#advice_view').val();
        post_data.qpos_pubkey = $('#qpos_pubkey_view').valid();
        post_data.used = $('#used_view').val();
        post_data.state = $('#state_view').val();

        $.ajax({
            url: '/posp/v1/api/terminal/view',
            type: 'POST',
            dataType: 'json',
            data: post_data,
            success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                    return false;
                }
                else {
                    toastr.success('保存修改成功');
                    $("#terminalViewForm").resetForm();
                    $("#terminalViewModal").modal('hide');
                    $('#terminalList').DataTable().draw();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });
});