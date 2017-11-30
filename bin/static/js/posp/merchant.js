/**
 * Created by admin on 2017/4/20.
 */
$(document).ready(function(){

    $.validator.addMethod("isMobile", function(value, element) {
        var length = value.length;
        var mobile = /^(1\d{10})$/;
        return this.optional(element) || (length === 11 && mobile.test(value));
    }, "请正确填写您的手机号码");

    $('#userList').DataTable({
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
            var $userList_length = $("#userList_length");
            var $userList_paginate = $("#userList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $userList_paginate.addClass('col-md-8');
            $userList_length.addClass('col-md-4');
            $userList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var se_userid = window.localStorage.getItem('myid');

            var get_data = {
                'page': Math.ceil(data.start / data.length) + 1,
                'maxnum': data.length,
                'se_userid': se_userid,
            };

            var mobile = $("#s_mobile").val();

            if(mobile){
                get_data.mobile = mobile;
            }

            var merchant_id = $("#s_merchant_id").val();
            if(merchant_id){
                get_data.merchant_id = merchant_id;
            }

            $.ajax({
                url: '/posp/v1/api/merchant/list',
                type: 'GET',
                dataType: 'json',
                data: get_data,
                success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#userList_processing");
                        $processing.css('display', 'none');
                        var resperr = data.resperr;
                        var respmsg = data.respmsg;
                        var msg = resperr ? resperr : respmsg;
                        toastr.warning(msg);
                        return false;
                    } else {
                        detail_data = data.data;
                        num = detail_data.num;
                        callback({
                            recordsTotal: num,
                            recordsFiltered: num,
                            data: detail_data.info
                        });
                    }
                },
                error: function(data) {
                    toastr.warning('请求数据异常');
                }

            });
        },
        'columnDefs': [
            {
                targets: 6,
                data: '操作',
                render: function(data, type, full) {
                    var userid = full.id;
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-userid="+userid+">"+'查看'+"</button>";
                    return view;
                }
            }
        ],
        'columns': [
            { data: 'id' },
            { data: 'name' },
            { data: 'mobile' },
            { data: 'idnumber' },
            { data: 'state' },
            { data: 'date_joined'},
        ],
        'oLanguage': {
            'sProcessing': '<span style="color:red;">加载中....</span>',
            'sLengthMenu': '每页显示_MENU_条记录',
            "sInfo": '显示 _START_到_END_ 的 _TOTAL_条数据',
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

    $("#userSearch").click(function(){

        var user_query_vt = $('#users_query').validate({
            rules: {
                s_merchant_id: {
                    required: false,
                },
                s_mobile: {
                    required: false,
                    // maxlength: 11
                    isMobile: '#s_mobile'
                },
            },
            messages: {
                s_merchant_id: {
                    required: '请输入商户ID'
                },
                s_mobile: {
                    required: '请输入手机号',
                    // maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
                },
            },
            errorPlacement: function(error, element){
                var $error_element = element.parent().parent().next();
                $error_element.text('');
                error.appendTo($error_element);
            }
        });
        var ok = user_query_vt.form();
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1400);
            return false;
        }
        $('#userList').DataTable().draw();
    });


    $(document).on('click', '.viewEdit', function(){
        $("label.error").remove();
        var se_userid = window.localStorage.getItem('myid');
        var userid = $(this).data('userid');
        $('#view_user_id').text(userid);

        var get_data = {};
        get_data.se_userid = se_userid;
        get_data.merchant_id = userid;
        $('#userViewForm').resetForm();
        $.ajax({
	        url: '/posp/v1/api/merchant/view',
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
                    return false;
                }
                else {
                    user_data = data.data;

                    $('#mobile').val(user_data.mobile);
                    $('#email').val(user_data.email);
                    $('#name').val(user_data.name);
                    $('#idnumber').val(user_data.idnumber);
                    $('#province').val(user_data.province);
                    $('#city').val(user_data.city);
                    $('#bankname').val(user_data.bankname);
                    $('#bankuser').val(user_data.bankuser);
                    $('#bankaccount').val(user_data.bankaccount);

                    $('#userViewModal').modal();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });

    });

    $('#userViewSubmit').click(function(){
        var user_edit_vt = $('#userViewForm').validate({
            rules: {
                mobile: {
                    required: true,
                    // maxlength: 16
                    isMobile: '#mobile'
                },
                email: {
                    required: true,
                    maxlength: 75
                },
                name: {
                    required: true,
                    maxlength: 32
                },
                idnumber: {
                    required: false,
                    maxlength: 20
                },
                province: {
                    required: false,
                    maxlength: 10
                },
                city: {
                    required: false,
                    maxlength: 32
                },
                bankname: {
                    required: false,
                    maxlength: 256
                },
                bankuser: {
                    required: false,
                    maxlength: 32
                },
                bankaccount: {
                    required: false,
                    maxlength: 32
                },
            },
            messages: {
                mobile: {
                    required: '请输入手机号',
                    // maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                email: {
                    required: '请输入邮箱',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                name: {
                    required: '请输入商户名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                idnumber: {
                    required: '请输入身份证号',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                province: {
                    required: '请输入省份',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                city: {
                    required: '请输入城市',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                bankname: {
                    required: '请输入开户行名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                bankuser: {
                    required: '请输入持卡人名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                bankaccount: {
                    required: '请输入银行账号',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
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

        var ok = user_edit_vt.form();
        if(!ok){
            return false;
        }

        var se_userid = window.localStorage.getItem('myid');

        var post_data = {}
        post_data.se_userid = se_userid;
        post_data.merchant_id = $('#view_user_id').text();
        post_data.mobile = $('#mobile').val();
        post_data.email = $('#email').val();
        post_data.name = $('#name').val();
        post_data.idnumber = $('#idnumber').val();
        post_data.province = $('#province').val();
        post_data.city = $('#city').val();
        post_data.bankname = $('#bankname').val();
        post_data.bankuser = $('#bankuser').val();
        post_data.bankaccount = $('#bankaccount').val();

        $.ajax({
	        url: '/posp/v1/api/merchant/view',
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
                    $("#userViewForm").resetForm();
                    $("#userViewModal").modal('hide');
                    $('#userList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });

    });

    $('#userCreate').click(function(){
        $('#userCreateForm').resetForm();
        $("label.error").remove();
        $('#userCreateModal').modal();
    });

    $('#userCreateSubmit').click(function(){

        var user_create_vt = $('#userCreateForm').validate({
            rules: {
                mobile_add: {
                    required: true,
                    // maxlength: 16
                    isMobile: '#mobile_add'
                },
                email_add: {
                    required: true,
                    maxlength: 75
                },
                name_add: {
                    required: true,
                    maxlength: 32
                },
                idnumber_add: {
                    required: false,
                    maxlength: 20
                },
                province_add: {
                    required: false,
                    maxlength: 10
                },
                city_add: {
                    required: false,
                    maxlength: 32
                },
                bankname_add: {
                    required: false,
                    maxlength: 256
                },
                bankuser_add: {
                    required: false,
                    maxlength: 32
                },
                bankaccount_add: {
                    required: false,
                    maxlength: 32
                },

            },
            messages: {
                mobile_add: {
                    required: '请输入手机号',
                    // maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                email_add: {
                    required: '请输入邮箱',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },

                name_add: {
                    required: '请输入商户名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                idnumber_add: {
                    required: '请输入身份证号',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                province_add: {
                    required: '请输入省份',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                city_add: {
                    required: '请输入城市',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                bankname_add: {
                    required: '请输入开户行名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                bankuser_add: {
                    required: '请输入持卡人名称',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
                },
                bankaccount_add: {
                    required: '请输入银行账号',
                    maxlength: $.validator.format("请输入一个 长度最多是 {0} 的字符串")
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

        var ok = user_create_vt.form();
        if(!ok){
            return false;
        }

        var se_userid = window.localStorage.getItem('myid');

        var post_data = {};
        post_data.se_userid = se_userid
        post_data.mobile = $('#mobile_add').val();
        post_data.email = $('#email_add').val();
        post_data.name = $('#name_add').val();
        post_data.idnumber = $('#idnumber_add').val();
        post_data.province = $('#province_add').val();
        post_data.city = $('#city_add').val();
        post_data.bankname = $('#bankname_add').val();
        post_data.bankuser = $('#bankuser_add').val();
        post_data.bankaccount = $('#bankaccount_add').val();

        $.ajax({
	        url: '/posp/v1/api/merchant/create',
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
                    toastr.success('添加成功');
                    $("#userCreateForm").resetForm();
                    $("#userCreateModal").modal('hide');
                    $('#userList').DataTable().draw();
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });

    });

});
