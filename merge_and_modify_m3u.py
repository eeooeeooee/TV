import re

def extract_channel_name(line):
    # 查找第一对引号中的内容
    match = re.search(r'"([^"]*)"', line)
    if match:
        channel_name = match.group(1)
    else:
        channel_name = ""
    # 去掉CCTV的破折号
    channel_name = re.sub(r'CCTV-', 'CCTV', channel_name)
    # 替换“经济科教”为“广东经济科教”
    channel_name = re.sub(r'经济科教', '广东经济科教', channel_name)
    return channel_name

def modify_channel_info(line):
    # 提取频道名称
    channel_name = extract_channel_name(line)
    # 添加tvg-id和tvg-logo
    tvg_id = tvg_name = channel_name
    tvg_logo = f'https://epg.112114.xyz/logo/{tvg_name}.png'
    new_info = f'tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}"'
    return re.sub(r'tvg-name="[^"]*"', new_info, line, count=1)

def process_m3u_file(file_path, output_file):
    with open(file_path, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('#EXTINF:'):
                # 修改频道信息
                line = modify_channel_info(line)
            elif line.startswith('rtp://'):
                # 修改地址格式
                line = re.sub(r'rtp://', 'http://192.168.1.1:9394/rtp/', line)
            outfile.write(line)

def merge_m3u_files(file1, file2, output_file):
    remove_first_line(file2)
    with open(output_file, 'w') as outfile:
        for fname in [file1, file2]:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

def remove_first_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        file.writelines(lines[1:])

# 下载文件并处理
file1 = 'GuangdongIPTV_rtp_4k.m3u'
file2 = 'GuangdongIPTV_rtp_hd.m3u'
merged_file = 'merged_GuangdongIPTV_rtp.m3u'
output_file = 'tv.m3u'

merge_m3u_files(file1, file2, merged_file)
process_m3u_file(merged_file, output_file)
