/**
     * 批量消费
     * @param records records
     * @param consumer consumer
     */
    @KafkaListener(topics = TOPIC_NAME_MEGATRON_VHR, groupId = "xxxGroupId")
    public void listenerBatchHandler(List<ConsumerRecord<String, String>> records, Consumer consumer) {
        log.info("Consumer.batch#size={}", records == null ? 0 : records.size());
        if (CollectionUtils.isEmpty(records)) {
            consumer.commitSync();
            return;
        }

        
        // 每次批量保存数量
        Integer batchSaveMax = 30;
        List<TFullSignalEntity> list = new ArrayList<>();
        for (int i = 0; i < records.size(); i++) {
            ConsumerRecord<String, String> record = records.get(i);
            String message = record.value();
            String vin = null;
            String userMessagId = null;
            if (StringUtils.isNotBlank(message)) {
                // 处理数据
                try {
                    TFullSignalEntity insertEntity = processMessage(message);
                    if (insertEntity == null) {
                        continue;
                    }
                    vin = insertEntity.getVin();
                    userMessagId = insertEntity.getUserMessageId();
                    list.add(insertEntity);
                    long startTime = System.currentTimeMillis();
                    if (list.size() >= batchSaveMax || i == records.size() - 1) {
						// 批量入库
                        vhrFullSignalDataMapper.batchInsert(list);
                        log.info("车辆:{},批量保存条:{}数据耗时:{}毫秒", vin, list.size(), (System.currentTimeMillis() - startTime));
                        list = new ArrayList<>();
                    }
                } catch (Exception e) {
                    log.error("车辆：{}，userMessagId:{} ,消息内容: {},消费kafka消息失败: {}", vin,
                            userMessagId, message, e, e.getMessage());
                }
            }
        }
        consumer.commitSync();
        log.info("Consumer end。");
    }

    /**
     * 消息
     * @param msg
     */
    public TFullSignalEntity processMessage(String msg) {
        if (StringUtils.isNotBlank(msg)) {
            JSONObject jsonObject = JSONUtil.parseObj(msg);
            String vin = jsonObject.getJSONObject("vehicleProperties").getStr("vin");

            String whiteVins = environment.getProperty("gdc.signal.whiteVins", String.class);
            if (StringUtils.isBlank(whiteVins) || !whiteVins.contains(vin)) {
                log.warn("vin:{}不在白名单中，数据不入库。", vin);
                return null;
            }

            String userMessageId = jsonObject.getStr("userMessageId");
            JSONObject payload = jsonObject.getJSONObject("payload");
            String signalName = payload.getStr("name");
            Object signalValue = payload.get("value");
            Long timestampObj = payload.getLong("timestamp");
            Object unitObj = payload.get("unit");
            Long ingestTimestamp = payload.getLong("ingest_timestamp");

            if (StringUtils.isBlank(signalName)) {
                log.error("vin: {}信号名为空：{}", vin, signalName);
                return null;
            }

            int dateTimeLength = 13;
            if (timestampObj != null && String.valueOf(timestampObj).length() == dateTimeLength) {
                timestampObj = (timestampObj / SystemConstant.A_THOUSAND) * SystemConstant.A_THOUSAND;
            }
            if (ingestTimestamp != null && String.valueOf(ingestTimestamp).length() == dateTimeLength) {
                ingestTimestamp = (ingestTimestamp / SystemConstant.A_THOUSAND) * SystemConstant.A_THOUSAND;
            }

        

            TFullSignalEntity fullSignalData = new TFullSignalEntity();
            fullSignalData.setVin(vin);
            fullSignalData.setName(signalName);
            fullSignalData.setValue(scienToStr(signalValue));
            fullSignalData.setUnit(String.valueOf(unitObj));
            fullSignalData.setUserMessageId(userMessageId);
            fullSignalData.setTimestamp(new Date(timestampObj));
            fullSignalData.setIngestTimestamp(new Date(ingestTimestamp));
            return fullSignalData;
        }
        return null;
    }

    /**
     * 科学计数法转字符串
     * @param signalValue
     * @return
     */
    private String scienToStr(Object signalValue) {
        if (ObjectUtils.isEmpty(signalValue)) {
            return "";
        }
        String strValue = String.valueOf(signalValue);
        // 科学法转字符串入库
        if (signalValue instanceof Number && strValue.matches(REGEX_SCIENTIFIC_NOTATION)) {
            strValue = new BigDecimal(strValue).toPlainString();
        }
        return strValue;
    }