# Independent source inspection — priority practice

Reviewer: priority-independent-review. Date: 2026-10-28.

This document records source inspection only. It is not an approval of any question.

- p1-d01 physical p40: visually inspected. Temperature/top_p/stop_sequences table; nucleus described briefly as top tokens totaling p probability. Does not define top-k sampling; the slide’s absolute “0=deterministic” wording must not be promoted into an absolute reproducibility claim.
- p2-t4-d01 p77: visually inspected BN normalization/learned affine formula; μ and variance, epsilon stabilizer, gamma/beta learned, LN per sample. Does not describe train/inference behavior.
- p2-t4-d02 p17: visually inspected BN per-channel batch+spatial axes; LN per-sample channels, GroupNorm groups; BN inference uses running training statistics, eval warning.
- p2-t4-d05 p21: visually inspected scalar predict/update and meaning of x,P,u,Q,z,R,K. P/R are variances. Equations x−=x+u;P−=P+Q;K=P−/(P−+R);x=x−+K(z−x−);P=(1−K)P−.
- p2-t4-d05 p27: visually inspected covariance ellipsoid example; not the full matrix recursion.
- p2-t4-d05 p28: visually inspected constant velocity F/H and matrix recursion x−=Fx;P−=FPFᵀ+Q;S=HP−Hᵀ+R;K=P−HᵀS⁻¹;x=x−+K(z−Hx−);P=(I−KH)P−.

Images: tmp/priority-review/{document-id}-{physical-page}.png. Original PDFs read without modification using bundled pypdfium2. More source pages are inspected when exact authored batches arrive.
