

import copy

def determineCorrpndPrice(character: str, post: dict) -> float:
    """ Xác định giá của `post` tương ứng với từng kí tự `character`

    Arguments:
        character {str} -- là một trong 4 kí tự A, B, C và D trong rule
        post {dict} -- dict chứa các thông tin của post

    Returns:
        float -- là giá tương ứng với kí tự
        None -- trong trường hợp bài post không có kí tự
    """
    price = None
    try:
        if character == 'A':
            price = post['price_A']
        elif character == 'B':
            price = post['price_B']
        elif character == 'C':
            price = post['price_C']
        else:
            price = post['price_D']
    except KeyError:
        pass

    return price

def verifyRule(rule: str, post) -> bool:
    """ Xác định xem bài `post` có thỏa mãn `rule` hay không

    Arguments:
        rule {str} -- xem ví dụ trong file Excel: https://docs.google.com/spreadsheets/d/1WnbgGt3wtzIyyyBB1tajdDvlMo_fg7nbmhOed3r0-Gw/edit#gid=0
        post {dict} -- dict chứa các thông tin của post

    Returns:
        bool -- True nếu bài `post` thỏa mãn `rule`
    """

    for i in range(0, len(rule) - 1, 1):
        if determineCorrpndPrice(rule[i], post) < determineCorrpndPrice(rule[i+1], post):
            return False

    return True

### Lưu ý: NÊN BỎ QUA HÀM NÀY MÀ ĐI THẲNG TỚI XEM XÉT STEP 3 Ở HÀM MAIN ###
def sort_by_rule(list_posts: list, input_rules: list):
    """Sắp xếp các bài post trong `list_posts` theo các rule đã định sẵn

    Arguments:
        list_posts {list} -- danh sách các bđs
        input_rules {list} -- danh sách các rules

    Returns:
        list - list các bài post sau khi đã sắp xếp theo rule
    """
    # list 'rules' chứa các luật (rule) dùng để sắp xếp.
    # Mỗi phần tử của list 'rules' có cấu trúc như sau:
    #   {
    #       'queue' : [],         # chứa danh sách các bài post ở trong 'list_posts` và thỏa mãn rule
    #       'rule' : "DBCA"       # là một string chứa rule
    #   }

    rules = copy.deepcopy(input_rules)


    ##################################################
    # Lặp từng bài post: với mỗi bài post phân loại các bài vào group tương ứng
    ##################################################
    for post in list_posts:
        # flag = False        ## Flag này sẽ toggle nếu bài post tìm được rule phù hợp

        for rule in rules:
            if verifyRule(rule['rule'], post):
                rule['queue'].append(post)
                # flag = True
                break

        # if not flag:
        #     ## nếu vào được đây chứng tỏ bài post
        #     ## không tìm được rule nào phù hợp
        #     ## Và post sẽ được append vào list riêng



    ##################################################
    # Serialize các group
    # đồng thời gán rank tương ứng và bỏ đi các trường price_A, price_B, price_C, price_D
    ##################################################

    ## Gộp các queue lại thành một queue duy nhất
    list_posts = []
    for rule in rules:
        list_posts = list_posts + rule['queue']

    ## gán rank và xóa các trường không cần thiết

    for rank, post in enumerate(list_posts):
        post['rank'] = rank


        ## Lý do ở đây tại sao lại bỏ các trường này mặc dù nó có cần thiết cho việc tính điểm
        ## là bởi vì dựa vào đặc tính của hàm tính điểm ban đầu, mình đã thu gọn nó về thành
        ## hàm tính điểm (getScore) bây giờ mà dùng đến thuộc tính 'case' của từng bđs
        ## thuộc tính 'case' được mình tính từ các thuộc tính priceA, B, C, D và priceRent

        del post['price_A']
        del post['price_B']
        del post['price_C']
        del post['price_D']
        del post['price_Rent']


    return list_posts
