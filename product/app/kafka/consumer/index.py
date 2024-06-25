import asyncio
from app.kafka.consumer.product import ProductConsumer
from app.kafka.consumer.category import CategoryConsumer
from app.kafka.consumer.brand import BrandConsumer
from app.core.config import settings

async def start_consumers():
    product_consumer = ProductConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="product_group")
    category_consumer = CategoryConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="category_group")
    brand_consumer = BrandConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="brand_group")

    await product_consumer.start()
    await category_consumer.start()
    await brand_consumer.start()

    await asyncio.gather(
        product_consumer.consume(),
        category_consumer.consume(),
        brand_consumer.consume()
    )

    await product_consumer.stop()
    await category_consumer.stop()
    await brand_consumer.stop()

if __name__ == "__main__":
    asyncio.run(start_consumers())
