from brownie import accounts, network, config, interface, PriceConsumerV3, MockV3Aggregator
import time
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork",
                             "mainnet-fork-dev", "ganache-local"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development"]


def main():
    deploy_and_consume_price_consumer()


def deploy_and_consume_price_consumer():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        eth_usd_price_feed = deploy_mockv3aggregator()
    else:
        eth_usd_price_feed = config["networks"][network.show_active(
        )]["eth_usd_price_feed"]
    print("Deploying PriceConsumerV3...")
    # how many decimals has the aggregator?
    price_feed_decimals = interface.AggregatorV3Interface(
        eth_usd_price_feed).decimals()
    price_consumer = PriceConsumerV3.deploy(
        eth_usd_price_feed, {"from": get_account()})
    print(f"Deployed at {price_consumer}...")
    latest_price = price_consumer.getLatestPrice()/(10 ** price_feed_decimals)
    print(
        f"The latest price of ETH/USD is ${latest_price}")


def deploy_mockv3aggregator():
    DECIMALS = 18
    # ETH has 18 decimals
    INITIAL_ANSWER = 3000*10**DECIMALS
    print(f"Deploying MockV3Aggregator on {network.show_active()}")
    mock = MockV3Aggregator.deploy(
        DECIMALS, INITIAL_ANSWER, {"from": get_account()})
    print(f"MockV3Aggregator deployed at {mock}")
    return mock.address


def get_account():
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
