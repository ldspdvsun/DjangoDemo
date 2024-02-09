"""
自定义的分页组件，以后如果想要使用这个分页组件，你需要做如下几件事：

在视图函数中：
    def pretty_list(request):

        # 1.根据自己的情况去筛选自己的数据
        queryset = models.PrettyNum.objects.all()

        # 2.实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html()       # 生成页码
        }
        return render(request, 'pretty_list.html', context)

在HTML页面中

    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>

"""
from django.utils.safestring import mark_safe
#
# class Pagination(object):
#
#     def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
#         """
#         :param request: 请求的对象
#         :param queryset: 符合条件的数据（根据这个数据进行分页处理）
#         :param page_size: 每页显示多少条数据
#         :param page_param: 在URL中传递的获取分页的参数，例如：/pretty/list/?page=12
#         :param plus: 显示当前页面的 前或后几页（页码）
#         """
#         # 获取当前页
#         page = request.GET.get(page_param, "1")
#         if page.isdecimal():
#             page = int(page)
#         else:
#             page = 1
#         self.page = page
#
#         # 获取每页显示数据条目，默认10
#         self.page_size = page_size
#         self.start = (page - 1) * page_size
#         self.end = page * page_size
#
#         self.page_queryset = queryset[self.start:self.end]
#
#         # 获取数据的总条数
#         total_count = queryset.count()
#
#         # 总页码
#         total_page_count, div = divmod(total_count, page_size)
#         if div:
#             total_page_count += 1
#         self.total_page_count = total_page_count
#         self.plus = plus
#
#     def html(self):
#         # 计算出显示当前页的前后5页
#         if self.total_page_count <= 2 * self.plus + 1:
#             start_page = 1
#             end_page = self.total_page_count
#         else:
#             # 数据库的数据比较多 > 11页
#             # 当前页<5时
#             if self.page <= self.plus:
#                 start_page = 1
#                 end_page = 2 * self.plus + 1
#             else:
#                 # 当前页 > 5
#                 # 当前页 + 5 > 总页
#                 if (self.page + self.plus) > self.total_page_count:
#                     start_page = self.total_page_count - 2 * self.plus
#                     end_page = self.total_page_count
#                 else:
#                     start_page = self.page - self.plus
#                     end_page = self.page + self.plus
#
#         # 页码
#         page_str_list = []
#         # 首页
#         first = f'<li><a href="?page={1}">首页</a></li>'
#         page_str_list.append(first)
#         # 上一页
#         if self.page > 1:
#             prev = f'<li><a href="?page={self.page - 1}">上一页</a></li>'
#         else:
#             prev = f'<li><a href="?page={self.page}">上一页</a></li>'
#         page_str_list.append(prev)
#
#         # 当前页 + 前后页面
#         for i in range(start_page, end_page + 1):
#             # 如果页码是当前页，显示着重显示page当前页
#             if i == self.page:
#                 ele = f'<li class="active"><a href="?page={i}">{i}</a></li>'
#             else:
#                 ele = f'<li><a href="?page={i}">{i}</a></li>'
#             page_str_list.append(ele)
#
#         # 下一页
#         if self.page < self.total_page_count:
#             suff = f'<li><a href="?page={self.page + 1}">下一页</a></li>'
#         else:
#             suff = f'<li><a href="?page={self.total_page_count}">下一页</a></li>'
#         page_str_list.append(suff)
#
#         # 尾页
#         last = f'<li><a href="?page={self.total_page_count}">尾页</a></li>'
#         page_str_list.append(last)
#
#         # 查询页面
#         search_string = """
#                    <li>
#                     <form method="get" style="float: right">
#                         <div class="input-group" style="width: 120px">
#                             <input type="text" name=page class="form-control" placeholder="页码">
#                             <span class="input-group-btn">
#                                 <button class="btn btn-default" type="submit">跳转</button>
#                             </span>
#                         </div>
#
#                     </form>
#                 </li>
#             """
#         page_str_list.append(search_string)
#
#         page_string = mark_safe("".join(page_str_list))
#         return page_string

# ================================
# 上下两个类的实现在于下面的类实现了在 搜索结果出来之后的基础上进行分页
# ================================
class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/etty/list/?page=12
        :param plus: 显示当前页的 前或后几页（页码）
        """

        from django.http.request import QueryDict
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param
        page = request.GET.get(page_param, "1")

        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    # def html(self):
    #     # 计算出，显示当前页的前5页、后5页
    #     if self.total_page_count <= 2 * self.plus + 1:
    #         # 数据库中的数据比较少，都没有达到11页。
    #         start_page = 1
    #         end_page = self.total_page_count
    #     else:
    #         # 数据库中的数据比较多 > 11页。
    #
    #         # 当前页<5时（小极值）
    #         if self.page <= self.plus:
    #             start_page = 1
    #             end_page = 2 * self.plus + 1
    #         else:
    #             # 当前页 > 5
    #             # 当前页+5 > 总页面
    #             if (self.page + self.plus) > self.total_page_count:
    #                 start_page = self.total_page_count - 2 * self.plus
    #                 end_page = self.total_page_count
    #             else:
    #                 start_page = self.page - self.plus
    #                 end_page = self.page + self.plus
    #
    #     # 页码
    #     page_str_list = []
    #
    #     self.query_dict.setlist(self.page_param, [1])
    #     page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
    #
    #     # 上一页
    #     if self.page > 1:
    #         self.query_dict.setlist(self.page_param, [self.page - 1])
    #         prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
    #     else:
    #         self.query_dict.setlist(self.page_param, [1])
    #         prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
    #     page_str_list.append(prev)
    #
    #     # 页面
    #     for i in range(start_page, end_page + 1):
    #         self.query_dict.setlist(self.page_param, [i])
    #         if i == self.page:
    #             ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
    #         else:
    #             ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
    #         page_str_list.append(ele)
    #
    #     # 下一页
    #     if self.page < self.total_page_count:
    #         self.query_dict.setlist(self.page_param, [self.page + 1])
    #         prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
    #     else:
    #         self.query_dict.setlist(self.page_param, [self.total_page_count])
    #         prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
    #     page_str_list.append(prev)
    #
    #     # 尾页
    #     self.query_dict.setlist(self.page_param, [self.total_page_count])
    #     page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
    #
    #     search_string = """
    #         <li>
    #             <form style="float: left;margin-left: -1px" method="get">
    #                 <input name="page"
    #                        style="position: relative;float:left;display: inline-block;width: 80px;border-radius: 0;"
    #                        type="text" class="form-control" placeholder="页码">
    #                 <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
    #             </form>
    #         </li>
    #         """
    #
    #     page_str_list.append(search_string)
    #     page_string = mark_safe("".join(page_str_list))
    #     return page_string

    def html(self):
        # 计算出，显示当前页的前5页、后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少，都没有达到11页。
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库中的数据比较多 > 11页。

            # 当前页<5时（小极值）
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页 > 5
                # 当前页+5 > 总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        # 首先添加样式居右显示
        page_str_list.append('<div class="pagination" style="float: right">')

        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 页面
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))


        search_string = """
            <li style="float: right;">
                <form style="float: left;margin-left: -1px" method="get">
                    <input name="page"
                           style="position: relative;float:left;display: inline-block;width: 80px;border-radius: 0;"
                           type="text" class="form-control" placeholder="页码">
                    <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                </form>
            </li>
            """

        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))

        page_str_list.append('</div>')
        return page_string

