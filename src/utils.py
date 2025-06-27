from order import OrderData

def print_order(p: OrderData) -> None:
    print(f"{'Field':<10} | {'Value'}")
    print("-" * 30)
    for field, value in p.__dict__.items():
        print(f"{field:<10} | {value}")