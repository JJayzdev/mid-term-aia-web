# Audit Track2

**35 approved,1 rejected** theo JSON. Hash12PDF khớp catalog; render95DPI và xem24trang gốc trong `tmp/reviewer/track2/`. MappingfolderRoot vẫn giữ xungđột bìa d03Phase1.

## Finding và retest

d11q01/d13q02 revision1 distractor vô nghĩa/xa nội dung, đã báo A1; revision2 đọc lại đúng các nhầm lẫn normalization/contract lân cận, approved. d03q01 gần trùng p1d03q01 nên rejected, yêu cầu tác giả đổi câu ứng dụng khác. Nhiều chỗ thiếu khoảng trắng được báo tác giả sửa, bản hiện hành cần bảo đảm UI dễ đọc.

## Từng câu

- **p2-t2-d01-q01 r1 approved**: p11: AIaaS fastest/noinfra,paypertoken,a đúng; physical/IaaS cầnops. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d01-q02 r1 approved**: p12: Team security/encryption/IAMleastprivilege,a/c đúng; hardware/hypervisor thuộcprovider. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d01-q03 r1 approved**: p11: Hybrid trainingIaaS/servingPaaS/prototypeAIaaS ghi chú cuối,true đúng. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d02-q01 r1 approved**: p9: Bronze insert-only, lưu cả3+whitespace,b đúng;trim/dedup/update trái cam kết. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d02-q02 r1 approved**: p13: RAG pinnedembedding,feature pointintime,a/d đúng; overwrite/singleGold trái bảng. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d02-q03 r1 approved**: p13: Mixed embedding coordinate systems nhiễu,a đúng;topk/dimension-only không bảo đảmversion. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d03-q01 r2 rejected**: p11: DynamicDecision đúng nguồn nhưng trùng đáng kể p1-d03-q01; yêu cầu đổi ứng dụngkhác. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d03-q02 r1 approved**: p13: One-step vàdeterministic/costerror cao anti-pattern,b/d đúng;adaptive/longhorizon ủng hộagent. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d03-q03 r1 approved**: p13: Benchmark rule/workflow/chatbot beforeagent ghi rõ,true đúng. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d04-q01 r1 approved**: p13: FAISS C++Pythonlibrary notserver,a đúng;DB/embeddingmodel/LLMonly sai loại. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d04-q02 r1 approved**: p16: DiskANN SSDgraph/IVFcluster,a/d đúng;HNSWram vàIVFretrainingdrift bácbỏb/c. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d04-q03 r1 approved**: p16: >100M cost-sensitiveDiskANN,d đúng; scenario chỉ đángbenchmark không claimbestabsolute. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d05-q01 r1 approved**: p6: Goodput request/s meetsTTFT/TPOT,a đúng; saturation/queue/batch khôngSLOservice. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d05-q02 r1 approved**: p12: Draftcandidates targetverify,continuousadmitperstep,a/b đúng;static/continuous đảo sai. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d05-q03 r1 approved**: p6: TTFTtofirsttoken vsTPOTintertoken,false đúng. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d06-q01 r1 approved**: p7: Tracking logparamsmetricsartifacts,a đúng;Registrylifecycle/Modelsformat/Projectsrepro khác. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d06-q02 r1 approved**: p13: Metrics khôngdata version soA/B vônghĩa,true đúng. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d06-q03 r1 approved**: p13/7: Run linkeddata version+snapshot/history resolvesoverwrite. Rubric c1linkedversion/c2replayversion,partial rõ,sum1; không bịa hiệu quả92/88 nguồn cóvídụ. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d07-q01 r1 approved**: p12: Contextbundle córetrieval/tool schema,a/c đúng;onlysystem/guardrailunversioned trái nguyên tắc. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d07-q02 r1 approved**: p15: Immutableversion movablelabel rollbackpointer,d đúng;overwrite/rebuild/deletehistory khôngtheo model. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d07-q03 r1 approved**: p15: Newimmutableversion+stagingproductionlabels,true đúng. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d08-q01 r1 approved**: p9: RPO lượngdata mất,a đúng;RTOdowntime khác. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d08-q02 r1 approved**: p16: Activepassive >5min/GPUbudget,a/c đúng;near0fullpool làactiveactive. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d08-q03 r1 approved**: p9: DifferentRTOdowntime/RPOloss+componentcost. Rubric hai khái niệm vàcomponentcost rõ,sum1. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d10-q01 r1 approved**: p14: MCP headers routing/quotaL7noparsebody,a đúng; không bypassauthz hoặc semanticallyverifyresult. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d10-q02 r1 approved**: p15: Toolquota+percallauthz,b/d đúng;sessiontrust/clientcatalog trái gateway. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d10-q03 r1 approved**: p15: Stateless identityperrequest,authzpercall,true đúng; scope thiết kế tài liệu. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d11-q01 r2 approved**: p9: Inference$/1Mtoken normalize,c đúng;revision2 dcost/requestwithoutlength/workload adjacentnormalizationerror acceptable. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d11-q02 r1 approved**: p16: Spot saveS3GCS andtestresume,c/d đúng;RAMonly/waitfailure trái bestpractice. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d11-q03 r1 approved**: p9: Training$/job explicit,true đúng; không kiểm chứng giácloud ngoài slide. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d12-q01 r1 approved**: p6: Freshness lastupdate/SLA,d đúng;schema/lineage/volume khác. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d12-q02 r1 approved**: p13: Rulesknowncontracts/anomalyunexpectedpatterns,a/d đúng;b/c đảo hay tuyệtđối sai. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d12-q03 r1 approved**: p6: Lineage origins/downstream,true đúng. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d13-q01 r1 approved**: p10: Audit tokencost/modelversion,a/c đúng;uptime/useronly khôngtrace request. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d13-q02 r2 approved**: p11: Consumersexpectedinterface,d đúng;revision2 providerdriven/snapshotassumption sai adjacentconcept. Đã xem trang gốc và đối chiếu explanation/options.
- **p2-t2-d13-q03 r1 approved**: p11: Faultinjectlatency/killpods/corruptdata checksdegradation,b đúng;happyonly/mocksuccess/compile khôngfailuretest. Đã xem trang gốc và đối chiếu explanation/options.

Chỉ audit câu/trang dẫn, không chứng nhận toàn bộ nội dung mỗiPDF. Nguồn dịch vụ/model/giá được hỏi theo slide; không kết luận thông số thị trường hiện hành. Không testapp ở lượt này.

## Retest d03q01 revision2

Đã đọc câu ứng dụng lowAgenticFit→chatbot/workflow,p11 hỗ trợ trực tiếp. Approvedrevision2,near-duplicateđóng. Tổnghiện hành36approved(3rev2+33rev1).
