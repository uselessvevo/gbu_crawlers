# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline


class GbuImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        # url = item['kwargs']['url'].split('/')[-2]
        name = item['kwargs']['name']
        number = item['kwargs']['number']
        image = request.url.split('/')[-1]
        path = f'{name}/images/{number}/{image}'

        return path
