# coding: utf-8

def gen_from_table(table_list, page, page_size):
    origin = [item[1] for item in table_list]
    count = sum(origin)
    judge = []
    judge_map = {}
    origin_snd = origin
    for i, v in enumerate(origin_snd):
        value = sum(origin_snd[:i + 1])
        judge.append(value)
        judge_map[value] = origin_snd[:i + 1]
    return count, origin, judge, judge_map


def gen_total_pages(count, page_size):
    pages, mod = divmod(count, page_size)
    if mod > 0:
        pages += 1
    return pages


def gen_page_range(pages, page_size):
    result = {}
    for i in range(1, pages):
        length = i * page_size
        ret = (length - page_size, length)
        result[i] = ret

    return result


def gen_table_list(judge, judge_map, page, page_range):
    page_conf = page_range.get(page)
    start, end = page_conf
    for item in judge:
        if item >= end:
            return judge_map[item]
        else:
            continue


def table_to_sql(tables, table_reverse_map, start, end):
    start_table = ''
    end_table = ''
    table_range_map = {}
    for table in tables:
        table_range_map[table] = None

    if len(tables) == 1:
        table_name = table_reverse_map.get(tables[0])
        print 'select from %s limit %s offset %s' % (table_name, end-start, start)
        v = tables[0]
        start_table = table_name
        end_table = table_name
        print 'start_table', start_table, 'end_table', end_table
        return {v: range(1, v)}, start_table, end_table
    else:
        before = 0
        count = sum(tables)
        count_range = range(1, count)
        for i, v in enumerate(tables):
            value = count_range[before:before+v]
            table_range_map[v] = value
            before += v

        for table in tables:
            value = table_range_map[table]
            if start in value:
                start_table = table_reverse_map[table]
            if end in value:
                end_table = table_reverse_map[table]
        return table_range_map, start_table, end_table


def gen_one_count_offset(table, start, end, table_map, table_range_map):
    return end-start, table_range_map[table_map[table]].index(start)


def gen_two_count_offset(start_table, end_table, start, end, table_map, table_range_map):
    ret = {}
    ret[start_table] = [abs(table_map[start_table]-start), table_range_map[table_map[start_table]].index(start+1)]
    ret[end_table] = [table_range_map[table_map[end_table]].index(end)+1, 0]
    return ret