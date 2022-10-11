import requests


def etukuri_search(term):
    url = "https://shop.etukuri.mv/products?search_type=https%3A%2F%2Fshop.etukuri.mv%2Fapi%2Fv1%2Fproducts&search=keyboard"
    base = "https://shop.etukuri.mv/"
    x = requests.session()
    x.get(base)
    direct = "https://shop.etukuri.mv/api/v1/users?fields=permalink%2Cthumb%2Cname%2Cslug&search=Keyboard"
    y = x.get(url)
    z = y.text.find('<meta name="csrf-token" content=')
    # print(z)
    zz = y.text.find('<title>')
    # print(zz)
    csrf_token = y.text[z + 33:zz]
    # print(y.text)
    csrf_token = csrf_token.replace('">', "")
    csrf_token = csrf_token.strip()
    print(csrf_token)
    main = f"https://shop.etukuri.mv/api/v1/products?fields=permalink%2Cthumb%2Cname%2Cslug&search={term}"
    headerx = {
        "authority": "shop.etukuri.mv",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "referer": f"https://shop.etukuri.mv/products?search_type=https^%^3A^%^2F^%^2Fshop.etukuri.mv^%^2Fapi^%^2Fv1^%^2Fproducts&search={term}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
                      "Safari/537.36 Edg/106.0.1370.42",
        "x-csrf-token": f"{csrf_token}",
        "x-requested-with": "XMLHttpRequest",
    }
    y = x.get(main, headers=headerx)
    products = y.json()['data']

    ret_data_list = []

    for i in range(len(products)):
        ret_data = {}
        bucket = products[i]["thumb"].split("/")

        ret_data['name'] = f"{products[i]['name']}"
        ret_data['link'] = f"{products[i]['permalink']}"
        ret_data['image'] = f"https://s3.amazonaws.com/s3.etukuri.mv/{bucket[4]}/{products[i]['media'][0]['file_name']}"

        ret_data_list.append(ret_data)
        # print(f"""
        # name = {products[i]['name']}
        # link = {products[i]['permalink']}
        # image =  https://s3.amazonaws.com/s3.etukuri.mv/{bucket[4]}/{products[i]['media'][0]['file_name']}
        # created_date = {products[i]['media'][0]['created_at']}
        # updated_date = {products[i]['media'][0]['updated_at']}
        # """)

    return ret_data_list
