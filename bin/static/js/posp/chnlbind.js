$(document).ready(function(){
    var table = $('#chnlbindList').DataTable({
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
            var $chnlbindList_length = $("#chnlbindList_length");
            var $chnlbindList_paginate = $("#chnlbindList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $chnlbindList_paginate.addClass('col-md-8');
            $chnlbindList_length.addClass('col-md-4');
            $chnlbindList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var userid = $("#s_userid").val();
            var mchntid = $("#s_mchntid").val();
            var termid = $("#s_termid").val();

            if(userid){
                get_data.userid = userid;
            }

            if(mchntid){
                get_data.mchntid = mchntid;
            }

            if(termid){
                get_data.termid = termid;
            }

            $.ajax({
	            url: '/posp/v1/api/channel/bind/list',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd !== '0000'){
                        $processing = $("#chnlbindList_processing");
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
                    var status = full.available;
                    var channel_bind_id =full.id;
                    var msg = status ? '打开' : '关闭';
                    var op = "<button type='button' class='btn btn-success btn-sm setStatus' data-channel_bind_id="+channel_bind_id+" data-status="+status+">"+msg+"</button>";
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-channel_bind_id="+channel_bind_id+">"+'查看'+"</button>";
                    return op+view;
                }
            }
        ],
		'columns': [
				{ data: 'userid'},
				{ data: 'priority'},
				{ data: 'name'},
				{ data: 'mchntid'},
				{ data: 'mchntnm'},
				{ data: 'termid'},
				{ data: 'available'}
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

    $(document).on('click', '.setStatus', function(){
        var channel_bind_id = $(this).data('channel_bind_id');
        var status = $(this).data('status');
        var value = status ? 0 : 1;
        var se_userid = window.localStorage.getItem('myid');
        var post_data = {
            'channel_bind_id': channel_bind_id,
            'available': value,
            'se_userid': se_userid
        };
        $.ajax({
	        url: '/posp/v1/api/channel/bind/switch',
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
                    $('#chnlbindList').DataTable().draw();
                    toastr.success('操作成功');
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
    });

    $("#chnlBindSearch").click(function(){
        var chnlbind_query_vt = $('#chnlbind_query').validate({
           rules: {
               s_userid: {
                   required: false,
                   maxlength: 20,
                   digits: true
               },
               s_mchntid: {
                   required: false,
                   maxlength: 30
               },
               s_termid: {
                   required: false,
                   maxlength: 30
               }
           },
           messages: {
               s_userid: {
                   required: '请输入商户ID',
                   maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
               },
               s_mchntid: {
                   required: '请输入商户号',
                   maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
               },
               s_termid: {
                   required: '请输入终端号',
                   maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
               },
           },
           errorPlacement: function(error, element){
               var $error_element = element.parent().parent().next();
               $error_element.text('');
               error.appendTo($error_element);
           }
        });
        var ok = chnlbind_query_vt.form();
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1400);
            return false;
        }
        $('#chnlbindList').DataTable().draw();
    });

    $(document).on('click', '.viewEdit', function(){
        $("label.error").remove();

        var se_userid = window.localStorage.getItem('myid');
        var channel_bind_id = $(this).data('channel_bind_id');
        $('#view_channel_bind_id').text(channel_bind_id);
        var get_data = {
            'se_userid': se_userid,
            'channel_bind_id': channel_bind_id
        };
        $.ajax({
	        url: '/posp/v1/api/channel/bind/view',
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
                    var bind = data.data;
                    set_channel(bind.chnlid);
                    $('#view_userid').val(bind.userid);
                    $('#view_priority').val(bind.priority);
                    $('#view_mchntid').val(bind.mchntid);
                    $('#view_termid').val(bind.termid);
                    $('#view_mchntnm').val(bind.mchntnm);
                    $('#view_tradetype').val(bind.tradetype);

                    $("#channelBindViewModal").modal();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
    });

    $('#channelBindViewSubmit').click(function(){

        var channel_bind_edit_vt = $('#channelBindViewForm').validate({
            rules: {
                view_priority: {
                    required: true,
                    digits:true
                },
                view_mchntid: {
                    required: false,
                    maxlength: 64
                },

                view_termid: {
                    required: false,
                    maxlength: 64
                },

                view_mchntnm: {
                    required: false,
                    maxlength: 64
                },

                view_tradetype: {
                    required: true,
                    digits: true
                }
            },
            messages: {
                view_priority: {
                    required: '请输入优先级',
                    digits: '请输入整数'
                },
                view_mchntid: {
                    required: '请输入商户号',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                view_termid: {
                    required: '请输入终端号',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                view_mchntnm: {
                    required: '请输入商户名',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                view_tradetype: {
                    required: '请输入交易类型',
                    digits: true
                },
            },
            errorPlacement: function(error, element){
                if(element.is(':checkbox')){
                    error.appendTo(element.parent().parent().parent());
                } else {
                    error.insertAfter(element);
                }
            }
        });
        var ok = channel_bind_edit_vt.form();
        if(!ok){
            return false;
        }

	    var post_data = {};
        var channel_bind_id = $('#view_channel_bind_id').text();
        var se_userid = window.localStorage.getItem('myid');
        post_data['se_userid'] = se_userid;

        post_data['channel_bind_id'] = channel_bind_id;
        post_data['userid'] = $('#view_userid').val();
		post_data['priority'] = $('#view_priority').val();
		post_data['available'] = $('#view_available').val();
		post_data['chnlid'] = $('#view_channel_name').val();
		post_data['termid'] = $('#view_termid').val();
		post_data['mchntid'] = $('#view_mchntid').val();
		post_data['mchntnm'] = $('#view_mchntnm').val();
		post_data['tradetype'] = $('#view_tradetype').val();

        $.ajax({
	        url: '/posp/v1/api/channel/bind/view',
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
                    $("#channelBindViewForm").resetForm();
                    $("#channelBindViewModal").modal('hide');
                    $('#chnlbindList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
    });

	$("#chnlBindCreate").click(function(){
        $("#channelBindCreateForm").resetForm();
        $("label.error").remove();
        get_channel();
		$("#channelBindCreateModal").modal();
	});

    $("#channelBindCreateSubmit").click(function(){

        var channel_bind_create_vt = $('#channelBindCreateForm').validate({
            rules: {
                add_userid: {
                    required: true,
                    digits:true
                },
                add_priority: {
                    required: true,
                    digits:true
                },
                add_mchntid: {
                    required: false,
                    maxlength: 64
                },
                add_termid: {
                    required: false,
                    maxlength: 64
                },
                add_mchntnm: {
                    required: false,
                    maxlength: 64
                },
                add_tradetype: {
                    required: true,
                    digits: true
                }
            },
            messages: {
                add_userid: {
                    required: '请输入商户ID',
                    digits: '请输入整数'
                },
                add_priority: {
                    required: '请输入优先级',
                    digits: '请输入整数'
                },
                add_mchntid: {
                    required: '请输入商户号',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                add_termid: {
                    required: '请输入终端号',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                add_mchntnm: {
                    required: '请输入商户名',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                add_tradetype: {
                    required: '请输入交易类型',
                    digits: true
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

        var ok = channel_bind_create_vt.form();
        if(!ok){
            return false;
        }

        var post_data = {};
        var se_userid = window.localStorage.getItem('myid');

        post_data['se_userid'] = se_userid;
        post_data['userid'] = $('#add_userid').val();
        post_data['priority'] = $('#add_priority').val();
        post_data['mchntid'] = $('#add_mchntid').val();
        post_data['termid'] = $('#add_termid').val();
        post_data['mchntnm'] = $('#add_mchntnm').val();
        post_data['tradetype'] = $('#add_tradetype').val();
        post_data['chnlid'] = $('#add_channel_name').val();

        $.ajax({
	        url: '/posp/v1/api/channel/bind/create',
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
                    toastr.success('添加通道绑定成功');
		            $("#channelBindCreateModal").modal('hide');
		            location.reload();
                    $('#chnlbindList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
    });

});


function get_channel() {
    $('#add_channel_name').html('');
    var se_userid = window.localStorage.getItem('myid');
    get_data = {};
    get_data.se_userid = se_userid;
    $.ajax({
        url: '/posp/v1/api/channel/names',
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
                var channel = data.data;
                for(var i=0; i<channel.length; i++) {
                    var channel_name = channel[i].name;
                    var channel_id = channel[i].id;
                    var option_str = '<option value='+channel_id + '>' + channel_name + '</option>';
                    $('#add_channel_name').append(option_str);
                }
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}

function set_channel(default_channel_id) {
    $('#view_channel_name').html('');
    var se_userid = window.localStorage.getItem('myid');
    get_data = {};
    get_data.se_userid = se_userid;
    $.ajax({
        url: '/posp/v1/api/channel/names',
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
                var channel = data.data;
                for(var i=0; i<channel.length; i++) {
                    var channel_name = channel[i].name;
                    var channel_id = channel[i].id;
                    var option_str = '<option value='+channel_id + '>' + channel_name + '</option>';
                    $('#view_channel_name').append(option_str);
                }
                $('#view_channel_name').val(default_channel_id);
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}