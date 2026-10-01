def test_open_order_occupies_table(client):
    table = client.post("/tables", json={"number": 1, "seats": 4}).json()
    category = client.post("/menu/categories", json={"name": "Mains"}).json()
    item = client.post(
        "/menu/items",
        json={"name": "Burger", "price": 9.5, "category_id": category["id"]},
    ).json()

    r = client.post("/orders", json={"table_id": table["id"]})
    assert r.status_code == 201
    assert r.json()["status"] == "open"

    table_check = client.get(f"/tables/{table['id']}").json()
    assert table_check["status"] == "occupied"


def test_full_workflow(client):
    table = client.post("/tables", json={"number": 1, "seats": 4}).json()
    category = client.post("/menu/categories", json={"name": "Mains"}).json()
    burger = client.post(
        "/menu/items",
        json={"name": "Burger", "price": 9.5, "category_id": category["id"]},
    ).json()
    fries = client.post(
        "/menu/items",
        json={"name": "Fries", "price": 4.5, "category_id": category["id"]},
    ).json()

    order = client.post("/orders", json={"table_id": table["id"]}).json()
    order_id = order["id"]

    client.post(f"/orders/{order_id}/items", json={"menu_item_id": burger["id"], "quantity": 2})
    client.post(f"/orders/{order_id}/items", json={"menu_item_id": fries["id"], "quantity": 1, "notes": "extra salt"})

    order_detail = client.get(f"/orders/{order_id}").json()
    assert order_detail["total"] == 23.5
    assert len(order_detail["items"]) == 2
    assert order_detail["items"][0]["total_price"] == 19.0
    assert order_detail["items"][1]["total_price"] == 4.5

    total = client.get(f"/orders/{order_id}/total").json()
    assert total["total"] == 23.5

    client.post(f"/orders/{order_id}/status/in_progress")
    client.get(f"/orders/{order_id}").json()

    client.post(f"/orders/{order_id}/status/served")

    payment = client.post(f"/payments/{order_id}", json={"method": "card"}).json()
    assert payment["amount"] == 23.5
    assert payment["method"] == "card"

    table_check = client.get(f"/tables/{table['id']}").json()
    assert table_check["status"] == "free"

    order_check = client.get(f"/orders/{order_id}").json()
    assert order_check["status"] == "paid"

    payment_lookup = client.get(f"/payments/{order_id}").json()
    assert payment_lookup["amount"] == 23.5


def test_cancel_frees_table(client):
    table = client.post("/tables", json={"number": 5, "seats": 2}).json()
    category = client.post("/menu/categories", json={"name": "Drinks"}).json()
    client.post(
        "/menu/items",
        json={"name": "Soda", "price": 2.5, "category_id": category["id"]},
    )

    order = client.post("/orders", json={"table_id": table["id"]}).json()
    order_id = order["id"]

    client.post(f"/orders/{order_id}/status/cancelled")

    table_check = client.get(f"/tables/{table['id']}").json()
    assert table_check["status"] == "free"

    order_check = client.get(f"/orders/{order_id}").json()
    assert order_check["status"] == "cancelled"


def test_cannot_add_items_to_paid_order(client):
    table = client.post("/tables", json={"number": 2, "seats": 2}).json()
    category = client.post("/menu/categories", json={"name": "Mains"}).json()
    item = client.post(
        "/menu/items",
        json={"name": "Burger", "price": 9.5, "category_id": category["id"]},
    ).json()

    order = client.post("/orders", json={"table_id": table["id"]}).json()
    order_id = order["id"]

    client.post(f"/orders/{order_id}/items", json={"menu_item_id": item["id"], "quantity": 1})
    client.post(f"/orders/{order_id}/status/in_progress")
    client.post(f"/orders/{order_id}/status/served")
    client.post(f"/payments/{order_id}", json={"method": "cash"})

    r = client.post(f"/orders/{order_id}/items", json={"menu_item_id": item["id"], "quantity": 1})
    assert r.status_code == 400


def test_invalid_status_transition(client):
    table = client.post("/tables", json={"number": 3, "seats": 2}).json()
    order = client.post("/orders", json={"table_id": table["id"]}).json()
    order_id = order["id"]

    r = client.post(f"/orders/{order_id}/status/paid")
    assert r.status_code == 400

    r = client.post(f"/orders/{order_id}/status/served")
    assert r.status_code == 400


def test_pay_without_items_fails(client):
    table = client.post("/tables", json={"number": 4, "seats": 2}).json()
    order = client.post("/orders", json={"table_id": table["id"]}).json()
    order_id = order["id"]

    client.post(f"/orders/{order_id}/status/in_progress")
    client.post(f"/orders/{order_id}/status/served")

    r = client.post(f"/payments/{order_id}", json={"method": "cash"})
    assert r.status_code == 400


def test_get_nonexistent_order(client):
    r = client.get("/orders/999")
    assert r.status_code == 404


def test_get_nonexistent_payment(client):
    r = client.get("/payments/999")
    assert r.status_code == 404


def test_table_not_found_for_order(client):
    r = client.post("/orders", json={"table_id": 999})
    assert r.status_code == 404


def test_menu_item_not_available(client):
    table = client.post("/tables", json={"number": 6, "seats": 2}).json()
    category = client.post("/menu/categories", json={"name": "Mains"}).json()
    item = client.post(
        "/menu/items",
        json={"name": "Burger", "price": 9.5, "category_id": category["id"]},
    ).json()

    client.patch(f"/menu/items/{item['id']}", json={"available": False})

    order = client.post("/orders", json={"table_id": table["id"]}).json()
    r = client.post(f"/orders/{order['id']}/items", json={"menu_item_id": item["id"], "quantity": 1})
    assert r.status_code == 400
