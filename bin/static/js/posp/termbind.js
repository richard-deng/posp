
$(document).ready(function(){

    var table = $('#termbindList').DataTable({
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
            var $termbindList_length = $("#termbindList_length");
            var $termbindList_paginate = $("#termbindList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $termbindList_paginate.addClass('col-md-8');
            $termbindList_length.addClass('col-md-4');
            $termbindList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var termbind_id = $("#s_termbind_id").val();
            var userid = $("#s_userid").val();

            if(termbind_id){
                get_data.terminalid = termbind_id;
            }

            if(userid){
                get_data.userid = userid;
            }

            $.ajax({
	            url: '/posp/v1/api/terminal/bind/list',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd !== '0000'){
                        $processing = $("#termbindList_processing");
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
                targets: 2,
                render: function(data, type, full) {
                    return split_key(data);
                }
            },
            {
                targets: 3,
                render: function(data, type, full) {
                    return split_key(data);
                }
            },
            {
                targets: 4,
                render: function(data, type, full) {
                    return split_key(data);
                }
            },
            {
                targets: 6,
                data: '操作',
                render: function(data, type, full) {
                    var termbind_id =full.id;
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-termbind_id="+termbind_id+">"+'查看'+"</button>";
                    return view;
                }
            }
        ],
		'columns': [
				{ data: 'userid'},
				{ data: 'terminalid'},
                { data: 'pinkey1'},
                { data: 'mackey'},
                { data: 'tmk'},
				{ data: 'state'}
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

    $("#termbindSearch").click(function(){
        var termbind_query_vt = $('#termbind_query').validate({
           rules: {
               s_terminal_id: {
                   required: false,
                   maxlength: 20,
                   digits: true
               },
               s_userid: {
                   required: false,
                   maxlength: 20,
                   digits: true
               }
           },
           messages: {
               s_terminal_id: {
                   required: '请输入通道ID',
                   maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串"),
                   digits: '请输入整数'
               },
               s_userid: {
                   required: '请输入商户ID',
                   maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串"),
                   digits: '请输入整数'
               }
           },
           errorPlacement: function(error, element){
               var $error_element = element.parent().parent().next();
               $error_element.text('');
               error.appendTo($error_element);
           }
        });
        var ok = termbind_query_vt.form();
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1000);
            return false;
        }
        $('#termbindList').DataTable().draw();
    });

    $("#termbindCreate").click(function(){
        $("#termbindCreateForm").resetForm();
        $("label.error").remove();
        $("#termbindCreateModal").modal();
    });

    $("#termbindCreateSubmit").click(function(){

        var termbind_create_vt = $('#termbindCreateForm').validate({
            rules: {
                /*
                active_date_add: {
                    required: false,
                    maxlength: 20
                },
                */
                userid_add: {
                    required: true,
                    maxlength: 11,
                    digits: true
                },
                terminal_id_add: {
                    required: true,
                    maxlength: 20
                },
                /*
                pinkey1_add: {
                    required: false,
                    maxlength: 32
                },
                pinkey2_add: {
                    required: false,
                    maxlength: 32
                },
                mackey_add: {
                    required: false,
                    maxlength: 32
                },
                tmk_add: {
                    required: false,
                    maxlength: 64
                },
                qpos_pubkey_add: {
                    required: false,
                    maxlength: 256
                }
                */
            },
            messages: {
                /*
                active_date_add: {
                    required: '请选择激活日期'
                },
                */
                userid_add: {
                    required: '请输入商户ID',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串"),
                    digits: '请输入整数'
                },
                terminal_id_add: {
                    required: '请输入终端ID',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                /*
                pinkey1_add: {
                    required: '请输入pinkey1',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                pinkey2_add: {
                    required: '请输入pinkey2',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                mackey_add: {
                    required: '请输入mackey',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                tmk_add: {
                    required: '请输入tmk',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                qpos_pubkey_add: {
                    required: '请输入公钥',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                }
                */
            },
            errorPlacement: function(error, element){
                if(element.is(':checkbox')){
                    error.appendTo(element.parent().parent().parent());
                } else {
                    error.insertAfter(element);
                }
            }
        });

        var ok = termbind_create_vt.form();
        if(!ok){
            return false;
        }

        var post_data = {};
        var se_userid = window.localStorage.getItem('myid');

        post_data.se_userid = se_userid;
        //post_data.active_date = $('#active_date_add').val();
        post_data.userid = $('#userid_add').val();
        post_data.terminalid = $('#terminal_id_add').val();
        //post_data.pinkey1 = $('#pinkey1_add').val();
        //post_data.pinkey2 = $('#pinkey2_add').val();
        //post_data.mackey = $('#mackey_add').val();
        //post_data.tmk = $('#tmk_add').val();
        //post_data.qpos_pubkey = $('#qpos_pubkey_add').val();

        $.ajax({
            url: '/posp/v1/api/terminal/bind/create',
            type: 'POST',
            dataType: 'json',
            data: post_data,
            success: function(data) {
                var respcd = data.respcd;
                if(respcd !== '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                    return false;
                }
                else {
                    toastr.success('添加终端绑定成功');
                    $("#termbindCreateModal").modal('hide');
                    location.reload();
                    $('#termbindList').DataTable().draw();
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
        var termbind_id = $(this).data('termbind_id');
        $('#view_termbind_id').text(termbind_id);
        var get_data = {
            'se_userid': se_userid,
            'termbind_id': termbind_id
        };
        $.ajax({
            url: '/posp/v1/api/terminal/bind/view',
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
                    console.log(data.data);

                    var bind = data.data;

                    //$('input[name=active_date_view]').val(bind.active_date);
                    $('#userid_view').val(bind.userid);
                    $('#terminal_id_view').val(bind.terminalid);
                    //$('#pinkey1_view').val(bind.pinkey1);
                    //$('#pinkey2_view').val(bind.pinkey2);
                    //$('#mackey_view').val(bind.mackey);
                    //$('#tmk_view').val(bind.tmk);
                    //$('#state_view').val(bind.state);
                    //$('#qpos_pubkey_view').val(bind.qpos_pubkey);

                    //$('#datetimepicker2').datetimepicker('update');

                    $("#termbindViewModal").modal();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });

    $('#termbindViewSubmit').click(function(){

        var termbind_edit_vt = $('#termbindViewForm').validate({
            rules: {
                /*
                active_date_view: {
                    required: false,
                    maxlength: 20
                },
                */
                userid_view: {
                    required: true,
                    maxlength: 11,
                    digits: true
                },
                terminal_id_view: {
                    required: true,
                    maxlength: 20
                },
                /*
                pinkey1_view: {
                    required: false,
                    maxlength: 32
                },
                pinkey2_view: {
                    required: false,
                    maxlength: 32
                },
                mackey_view: {
                    required: false,
                    maxlength: 32
                },
                tmk_view: {
                    required: false,
                    maxlength: 32
                },
                qpos_pubkey_view: {
                    required: false,
                    maxlength: 256
                }
                */
            },
            messages: {
                /*
                active_date_view: {
                    required: '请选择激活日期'
                },
                */
                userid_view: {
                    required: '请输入商户ID',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串"),
                    digits: '请输入整数'
                },
                terminal_id_view: {
                    required: '请输入终端ID',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                /*
                pinkey1_view: {
                    required: '请输入pinkey1',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                pinkey2_view: {
                    required: '请输入pinkey2',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                mackey_view: {
                    required: '请输入mackey',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                tmk_view: {
                    required: '请输入tmk',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                qpos_pubkey_view: {
                    required: '请输入公钥',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                }
                */
            },
            errorPlacement: function(error, element){
                if(element.is(':checkbox')){
                    error.appendTo(element.parent().parent().parent());
                } else {
                    error.insertAfter(element);
                }
            }
        });
        var ok = termbind_edit_vt.form();
        if(!ok){
            return false;
        }

        var post_data = {};
        var termbind_id = $('#view_termbind_id').text();
        var se_userid = window.localStorage.getItem('myid');

        post_data.se_userid = se_userid;
        post_data.termbind_id = termbind_id;

        //post_data.active_date = $('#active_date_view').val();
        post_data.userid = $('#userid_view').val();
        post_data.terminalid = $('#terminal_id_view').val();
        //post_data.pinkey1 = $('#pinkey1_view').val();
        //post_data.pinkey2 = $('#pinkey2_view').val();
        //post_data.mackey = $('#mackey_view').val();
        //post_data.tmk = $('#tmk_view').val();
        //post_data.qpos_pubkey = $('#qpos_pubkey_view').val();
        //post_data.state = $('#state_view').val();

        $.ajax({
            url: '/posp/v1/api/terminal/bind/view',
            type: 'POST',
            dataType: 'json',
            data: post_data,
            success: function(data) {
                var respcd = data.respcd;
                if(respcd !== '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                    return false;
                }
                else {
                    toastr.success('保存修改成功');
                    $("#termbindlViewForm").resetForm();
                    $("#termbindViewModal").modal('hide');
                    $('#termbindList').DataTable().draw();
                }
            },
            error: function(data) {
                toastr.warning('请求异常');
            }
        });
    });
});