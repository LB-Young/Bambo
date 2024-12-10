import aiohttp
import json
from lxml import html
import asyncio

async def get_paper_detail(session, base_url, paper_url):
    """获取论文详细信息"""
    try:
        async with session.get(paper_url) as response:
            if response.status != 200:
                return None
            detail_html = await response.text()
            tree = html.fromstring(detail_html)
            
            # 获取摘要              
            abstract = tree.xpath('/html/body/div[3]/main/div[2]/div/div/p/text()')
            abstract = abstract[0].strip() if abstract else "无摘要"
            
            # 获取日期
            date = tree.xpath('/html/body/div[3]/main/div[1]/div/div/div/p/span[1]/text()')
            date = date[0].strip() if date else "未知日期"
            
            # 获取star数        /html/body/div[3]/main/div[3]/div[1]/div[2]/div[1]/div/div[2]/div/text()
            stars = tree.xpath('/html/body/div[3]/main/div[3]/div[1]/div[2]/div[1]/div/div[2]/div/text()')
            stars = int(''.join(stars).strip()) if stars else 0
            
            return {
                'abstract': abstract,
                'published_date': date,
                'stars': stars
            }
    except Exception as e:
        print(f"获取论文详情失败: {str(e)}")
        return None

async def paper_search(nums: int = 10, params_format: bool = False):
    """
    获取 Papers with Code 网站今日发布的论文信息
    
    Args:
        max_results: 最大返回结果数
        params_format: 是否返回参数格式
    
    Returns:
        list: 论文信息列表，每个元素包含标题、作者、发表时间、摘要和star数
    """
    if params_format:
        return ['nums']
        
    try:
        base_url = "https://paperswithcode.com"
        url = f"{base_url}/latest"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"HTTP错误: {response.status}")
                    
                html_content = await response.text()
                tree = html.fromstring(html_content)
                papers = []
                
                # 获取论文列表
                for i in range(1, nums + 1):
                    try:
                        # 获取标题和链接
                        title_xpath = f'/html/body/div[3]/div[2]/div[{i}]/div[2]/div/div[1]/h1/a'
                        title_elem = tree.xpath(title_xpath)
                        
                        if not title_elem:
                            continue
                            
                        title = title_elem[0].text.strip()
                        paper_url = base_url + title_elem[0].get('href')
                        
                        # 获取详细信息
                        detail_info = await get_paper_detail(session, base_url, paper_url)
                        
                        if detail_info:
                            papers.append({
                                'title': title,
                                'url': paper_url,
                                'abstract': detail_info['abstract'],
                                'published_date': detail_info['published_date'],
                                'stars': detail_info['stars']
                            })
                            
                    except Exception as e:
                        print(f"处理第{i}篇论文时出错: {str(e)}")
                        continue
                
                return papers
                
    except Exception as e:
        raise Exception(f"获取Papers with Code论文失败: {str(e)}")
