# hc2pm
将HttpCanary App导出的request.json转换为Postman可识别导入的格式

### 使用

```
python hc2pm.python -i httpcanary_requests/ -c postman_collection -o result.json
```

可使用参数：

- `-h`: 查看帮助
- `-i`: 待转换文件/目录，必须
- `-c`: postman中的collection名称
- `-o`: 结果输出文件
