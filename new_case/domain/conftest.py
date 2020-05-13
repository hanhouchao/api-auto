import time

from common.settings import RESOURCE_PREFIX, REGION_NAME, PROJECT_NAME

time_base = time.time()
full_casename = ["有指定项目有集群", "无集群无项目", "有集群分配到全部项目", "有集群指定不存在的项目", "指定不存在的集群指定项目"]
full_data_list = [
    {'timestamp': str(round(time_base * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-full".format(RESOURCE_PREFIX),
     'kind': 'full',
     'region_name': REGION_NAME,
     'project_name': PROJECT_NAME
     },
    {'timestamp': str(round((time_base + 100) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-full-none".format(RESOURCE_PREFIX),
     'kind': 'full',
     'region_name': '',
     'project_name': ''
     },
    {'timestamp': str(round((time_base + 200) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-full-all".format(RESOURCE_PREFIX),
     'kind': 'full',
     'region_name': REGION_NAME,
     'project_name': 'ALL_ALL'
     },
    {'timestamp': str(round((time_base + 300) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-full-errorpro".format(RESOURCE_PREFIX),
     'kind': 'full',
     'region_name': REGION_NAME,
     'project_name': 'errorproject'
     },
    {'timestamp': str(round((time_base + 400) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-full-errorreg".format(RESOURCE_PREFIX),
     'kind': 'full',
     'region_name': 'errorregion',
     'project_name': PROJECT_NAME
     },
]
ext_casename = ["有指定项目有集群", "无集群无项目", "有集群分配到全部项目", "有集群指定不存在的项目", "指定不存在的集群指定项目"]
ext_data_list = [
    {'timestamp': str(round((time_base + 1000) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-ext".format(RESOURCE_PREFIX),
     'kind': 'extensive',
     'region_name': REGION_NAME,
     'project_name': PROJECT_NAME
     },
    {'timestamp': str(round((time_base + 1100) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-ext-none".format(RESOURCE_PREFIX),
     'kind': 'extensive',
     'region_name': '',
     'project_name': ''
     },
    {'timestamp': str(round((time_base + 1200) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-ext-all".format(RESOURCE_PREFIX),
     'kind': 'extensive',
     'region_name': REGION_NAME,
     'project_name': 'ALL_ALL'
     },
    {'timestamp': str(round((time_base + 1300) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-errorpro".format(RESOURCE_PREFIX),
     'kind': 'extensive',
     'region_name': REGION_NAME,
     'project_name': 'errorproject'
     },
    {'timestamp': str(round((time_base + 1400) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-ext-errorreg".format(RESOURCE_PREFIX),
     'kind': 'extensive',
     'region_name': 'errorregion',
     'project_name': PROJECT_NAME
     },
]
update_casename = ["全域名更新到无集群无项目", "全域名更新到有集群分配到全部项目", "全域名更新到有集群指定项目",
                   "泛域名更新到无集群无项目", "泛域名更新到有集群分配到全部项目", "泛域名更新到有集群指定项目"]

patch_data_list = [
    {'timestamp': str(round(time_base * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-full".format(RESOURCE_PREFIX),
     'kind': 'full',
     'region_name': '',
     'project_name': ''
     },
    {'timestamp': str(round((time_base + 100) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-full-none".format(RESOURCE_PREFIX),
     'kind': 'full',
     'region_name': REGION_NAME,
     'project_name': 'ALL_ALL'
     },
    {'timestamp': str(round((time_base + 200) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-full-all".format(RESOURCE_PREFIX),
     'kind': 'full',
     'region_name': REGION_NAME,
     'project_name': PROJECT_NAME
     },
    {'timestamp': str(round((time_base + 1000) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-ext".format(RESOURCE_PREFIX),
     'kind': 'extensive',
     'region_name': '',
     'project_name': ''
     },
    {'timestamp': str(round((time_base + 1100) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-ext-none".format(RESOURCE_PREFIX),
     'kind': 'extensive',
     'region_name': REGION_NAME,
     'project_name': 'ALL_ALL'
     },
    {'timestamp': str(round((time_base + 1200) * 10000)).zfill(24),
     'name': "{}-ares-acp-domain-ext-all".format(RESOURCE_PREFIX),
     'kind': 'extensive',
     'region_name': REGION_NAME,
     'project_name': PROJECT_NAME
     }
]
