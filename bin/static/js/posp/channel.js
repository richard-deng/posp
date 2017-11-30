$(document).ready(function(){
    search_source();
    $.validator.addMethod("isMobile", function(value, element) {
        var length = value.length;
        var mobile = /^(1\d{10})$/;
        return this.optional(element) || (length == 11 && mobile.test(value));
    }, "请正确填写您的手机号码");

    $.validator.addMethod("isPhone", function(value, element) {
        var tel_pattern =  /^\d{3,4}-\d{7,8}(-\d{3,4})?$/;
        var mobile_pattern = /^(1\d{10})$/;
        return this.optional(element) || (tel_pattern.test(value)|| mobile_pattern.test(value));
    }, "请正确填写您的电话号码");

    $.validator.addMethod("isYuan", function(value, element) {
        var length = value.length;
        // var yuan  = /^([0-9]{1,6})\.([0-9]{1,2})$/;
        var yuan = /^([0-9]{1,8})(.([0-9]{1,2})){0,1}$/;
        return this.optional(element) || (length && yuan.test(value) && parseFloat(value) > 0);
    }, "请正确填写您的价格");

    $.validator.addMethod("isLessOne", function(value, element) {
        var length = value.length;
        var less_one  = /^(0)\.([0-9]{1,2})$/;
        return this.optional(element) || (length && less_one.test(value));
    }, "请正确填写您的比例");

    var table = $('#channelList').DataTable({
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
            var $channelList_length = $("#channelList_length");
            var $channelList_paginate = $("#channelList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $channelList_paginate.addClass('col-md-8');
            $channelList_length.addClass('col-md-4');
            $channelList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var channel_name = $("#s_channel_name").val();

            if(channel_name){
                get_data.name = channel_name;
            }

            $.ajax({
	            url: '/posp/v1/api/channel/list',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd !== '0000'){
                        $processing = $("#channelList_processing");
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
                targets: 1,
                render: function(data, type, full) {
                    return split_key(data);
                }
            },
            {
                targets: 2,
                render: function(data, type, full) {
                    return split_key(data);
                }
            },
            {
                targets: 7,
                data: '操作',
                render: function(data, type, full) {
                    var status = full.available;
                    var uid =full.userid;
                    var channel_id =full.id;
                    var msg = status ? '打开' : '关闭';
                    var op = "<button type='button' class='btn btn-success btn-sm setStatus' data-channelid="+channel_id+" data-status="+status+">"+msg+"</button>";
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-uid="+uid+" data-channelid="+channel_id+">"+'查看'+"</button>";
                    return op+view;
                }
            }
        ],
		'columns': [
				{ data: 'name'},
                { data: 'zmk'},
				{ data: 'zpk'},
				{ data: 'chcd'},
				{ data: 'inscd'},
				{ data: 'code'},
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

	$("#channelCreate").click(function(){
        $("#channelCreateForm").resetForm();
        $("label.error").remove();
		$("#channelCreateModal").modal();
	});

    $("#channelNameSearch").click(function(){
        var channel_query_vt = $('#channel_query').validate({
           rules: {
               q_channel_name: {
                   required: false,
                   maxlength: 256
               }
           },
           messages: {
               q_channel_name: {
                   required: '请输入通道名称',
                   maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
               }
           },
           errorPlacement: function(error, element){
               var $error_element = element.parent().parent().next();
               $error_element.text('');
               error.appendTo($error_element);
           }
        });
        var ok = channel_query_vt.form();
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1400);
            return false;
        }
        $('#channelList').DataTable().draw();
    });

    $("#channelCreateSubmit").click(function(){

        var channel_create_vt = $('#channelCreateForm').validate({
            rules: {

                channel_name_add: {
                    required: true,
                    maxlength: 32
                },

                zmk_add: {
                    required: false,
                    maxlength: 36
                },

                zpk_add: {
                    required: false,
                    maxlength: 36
                },

                chcd_add: {
                    required: false,
                    maxlength: 16
                },

                inscd_add: {
                    required: false,
                    maxlength: 16
                },

                code_add: {
                    required: false,
                    maxlength: 4
                },

                route_add: {
                    required: false,
                    maxlength: 32
                },

                mchntid_add: {
                    required: false,
                    maxlength: 32
                },

                mchntnm_add: {
                    required: false,
                    maxlength: 32
                },

                tdkey_add: {
                    required: false,
                    maxlength: 36
                },

                mackey_add: {
                    required: false,
                    maxlength: 36
                },

                terminal_id_add: {
                    required: false,
                    maxlength: 32
                }

            },
            messages: {

                channel_name_add: {
                    required: '请输入通道名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                zmk_add: {
                    required: '请输入通道主秘钥',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                zpk_add: {
                    required: '请输入通道工作秘钥',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                chcd_add: {
                    required: '请输入平台分配机构号',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                inscd_add: {
                    required: '请输入接入路由分配机构',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                code_add: {
                    required: '请输入通道代码',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                route_add: {
                    required: '请输入路由',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                mchntid_add: {
                    required: '请输入通道商户ID',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                mchntnm_add: {
                    required: '请输入通道商户名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                tdkey_add: {
                    required: '请输入Tdkey',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                mackey_add: {
                    required: '请输入Mackey',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                terminal_id_add: {
                    required: '请输入终端ID',
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

        var ok = channel_create_vt.form();
        if(!ok){
            return false;
        }

        var post_data = {};
        var se_userid = window.localStorage.getItem('myid');

        post_data['se_userid'] = se_userid;
        post_data['name'] = $('#channel_name_add').val();
		post_data['zmk'] = $('#zmk_add').val();
		post_data['zpk'] = $('#zpk_add').val();
		post_data['chcd'] = $('#chcd_add').val();
		post_data['inscd'] = $('#inscd_add').val();
		post_data['code'] = $('#code_add').val();
		post_data['route'] = $('#route_add').val();
		post_data['mchntid'] = $('#mchntid_add').val();
		post_data['mchntnm'] = $('#mchntnm_add').val();
		post_data['tdkey'] = $('#tdkey_add').val();
		post_data['mackey'] = $('#mackey_add').val();
		post_data['terminalid'] = $('#terminal_id_add').val();

        $.ajax({
	        url: '/posp/v1/api/channel/create',
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
                    toastr.success('添加通道成功');
                    search_source();
		            $("#channelCreateModal").modal('hide');
		            location.reload();
                    $('#channelList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
    });

    $(document).on('click', '.viewEdit', function(){
        $("label.error").remove();
        //var uid = $(this).data('uid');
        var se_userid = window.localStorage.getItem('myid');
        var channel_id = $(this).data('channelid');
        $('#view_channel_id').text(channel_id);
        var get_data = {
            'se_userid': se_userid,
            'channel_id': channel_id
        };
        $.ajax({
	        url: '/posp/v1/api/channel/view',
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

                    var channel = data.data;

                    $('#channel_name').val(channel.name);
                    $('#zmk').val(channel.zmk);
                    $('#zpk').val(channel.zpk);
                    $('#chcd').val(channel.chcd);
                    $('#inscd').val(channel.inscd);
                    $('#code').val(channel.code);
                    $('#route').val(channel.route);
                    $('#mchntid').val(channel.mchntid);
                    $('#mchntnm').val(channel.mchntnm);
                    $('#tdkey').val(channel.tdkey);
                    $('#mackey').val(channel.mackey);
                    $('#terminal_id').val(channel.terminalid);

                    $("#channelViewModal").modal();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
    });

    $(document).on('click', '.setStatus', function(){
        var channel_id = $(this).data('channelid');
        var status = $(this).data('status');
        var value = status ? 0 : 1;
        var se_userid = window.localStorage.getItem('myid');
        var post_data = {
            'channel_id': channel_id,
            'state': value,
            'se_userid': se_userid
        };
        $.ajax({
	        url: '/posp/v1/api/channel/state/change',
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
                    $('#channelList').DataTable().draw();
                    toastr.success('操作成功');
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
    });

    $('#channelViewSubmit').click(function(){

        var channel_edit_vt = $('#channelViewForm').validate({
            rules: {
                channel_name: {
                    required: true,
                    maxlength: 32
                },
                zmk: {
                    required: false,
                    maxlength: 36
                },

                zpk: {
                    required: false,
                    maxlength: 36
                },

                chcd: {
                    required: false,
                    maxlength: 16
                },

                inscd: {
                    required: false,
                    maxlength: 16
                },

                code: {
                    required: false,
                    maxlength: 4
                },

                route: {
                    required: false,
                    maxlength: 32
                },

                mchntid: {
                    required: false,
                    maxlength: 32
                },

                mchntnm: {
                    required: false,
                    maxlength: 32
                },

                tdkey: {
                    required: false,
                    maxlength: 36
                },

                mackey: {
                    required: false,
                    maxlength: 36
                },

                terminal_id: {
                    required: false,
                    maxlength: 32
                }

            },
            messages: {
                channel_name: {
                    required: '请输入通道名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                zmk: {
                    required: '请输入通道主秘钥',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                zpk: {
                    required: '请输入通道工作秘钥',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                chcd: {
                    required: '请输入平台分配机构号',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                inscd: {
                    required: '请输入接入路由分配机构',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                code: {
                    required: '请输入通道代码',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                route: {
                    required: '请输入路由',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                mchntid: {
                    required: '请输入通道商户ID',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                mchntnm: {
                    required: '请输入通道商户名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                tdkey: {
                    required: '请输入Tdkey',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                mackey: {
                    required: '请输入Mackey',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                terminal_id: {
                    required: '请输入终端ID',
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
        var ok = channel_edit_vt.form();
        if(!ok){
            return false;
        }

	    var post_data = {};
        var channel_id = $('#view_channel_id').text();
        var se_userid = window.localStorage.getItem('myid');
        post_data['se_userid'] = se_userid;

        post_data['channel_id'] = channel_id;

		post_data['name'] = $('#channel_name').val();
		post_data['available'] = $('#available').val();
		post_data['zmk'] = $('#zmk').val();
		post_data['zpk'] = $('#zpk').val();
		post_data['chcd'] = $('#chcd').val();
		post_data['inscd'] = $('#inscd').val();
		post_data['code'] = $('#code').val();
		post_data['route'] = $('#route').val();
		post_data['mchntid'] = $('#mchntid').val();
		post_data['mchntnm'] = $('#mchntnm').val();
		post_data['tdkey'] = $('#tdkey').val();
		post_data['mackey'] = $('#mackey').val();
		post_data['terminalid'] = $('#terminal_id').val();

        $.ajax({
	        url: '/posp/v1/api/channel/view',
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
                    $("#channelViewForm").resetForm();
                    $("#channelViewModal").modal('hide');
                    $('#channelList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
    });


});

function search_source() {
    var get_data = {};
    var se_userid = window.localStorage.getItem('myid');
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
                var subjects = new Array();
                for(var i=0; i<data.data.length; i++){
                    subjects.push(data.data[i].name)
                }
                $('#s_channel_name').typeahead({source: subjects});
            }
        },
        error: function(data) {
            toastr.warning('请求异常');
        }
    });
}

function split_key(key) {
    if(key === null){
        return '';
    }
    var len = key.length;
    if(len > 16){
        return key.slice(0,16)+'<br>' + key.slice(16, -1);
    } else {
        return key;
    }
}
