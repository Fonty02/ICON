light_l1.
light_l2.
ok_l1.
ok_l2.
ok_cb1.
ok_cb2.
dark_l1.
dark_l2.
up_s1.
down_s1.
up_s2.
down_s2.
up_s3.
down_s3.
live_outside.
live_l1 :- live_w0.
live_w0 :- live_w1 , up_s2.
live_w0 :- live_w2 , down_s2.
live_w1 :- live_w3 , up_s1.
live_w2 :- live_v3 , down_s1.
live_l2 :- live_w4.
live_w4 :- live_w3 , up_s3.
live_p1 :- live_w3.
live_w3 :- live_w5 , ok_cb1.
live_p2 :- live_w6.
live_w6 :- live_w5 , ok_cb2.
live_w5 :- live_outside.
lit_l1 :- light_l1 , live_l1 , ok_l1.
lit_l2 :- light_l2 , live_l2 , ok_l2.
false :- dark_l1 , lit_l1
false :- dark_l2 , lit_l2