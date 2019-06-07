Methodology
-----------

- AS set sizes per IXP and peering LAN prefix sizes from peeringdb.com (https://www.peeringdb.com/api/ixlan?depth=2)
- Data as of June 3rd 2019
- Data set includes 672 IXPs and information on 726 peering LANs 
- Required IPs per IXP are assumed to be twice the size of IXP's AS set (i.e., 100% overprovisioning)
- Analysis can be reproduced by running the analysis.py script in this git project. To pull in more recent data from
peeringdb you can delete data.json and run the script.

Distribution of peering LAN sizes
---------------------------------

This analysis shows the distribution of current peering LAN prefix sizes.

![peering LAN prefix size distribution](peering_lan_prefix_size.png)
(Figure 1)

<!---
Corresponding data:

```
+---------------+------------------+----------------------+----------------------+--------------------------+
| Prefix size   |   # Peering LANs |   # Peering LANs cum | # Peering LANs rel   | # Peering LANs rel cum   |
|---------------+------------------+----------------------+----------------------+--------------------------|
| /20           |                2 |                    2 | 0.28%                | 0.28%                    |
| /21           |                8 |                   10 | 1.10%                | 1.38%                    |
| /22           |               25 |                   35 | 3.44%                | 4.82%                    |
| /23           |               76 |                  111 | 10.47%               | 15.29%                   |
| /24           |              536 |                  647 | 73.83%               | 89.12%                   |
| /25           |               38 |                  685 | 5.23%                | 94.35%                   |
| /26           |               29 |                  714 | 3.99%                | 98.35%                   |
| /27           |               11 |                  725 | 1.52%                | 99.86%                   |
| /28           |                1 |                  726 | 0.14%                | 100.00%                  |
+---------------+------------------+----------------------+----------------------+--------------------------+
(Table 1)
```
-->

Theoretical minimum peering LAN sizes/IXP
-----------------------------------------

This analysis shows which fraction of IXPs in peeringDB would theoretically fit into a /27, /26, ..., /21. It is based
on the assumption that an IXP operator requires 2 times the number of connected ASes IPs to operate a peering LAN.

![peering LAN prefix size distribution](required_ips_per_ixp.png)
(Figure 2)

<!---
```
+------------------+--------------------+----------+--------------+------------+----------------+
| # req. IPs/IXP   | min. prefix size   |   # IXPs |   # IXPs cum | IXPs rel   | IXPs rel cum   |
|------------------+--------------------+----------+--------------+------------+----------------|
| <32              | </27               |      398 |          398 | 59.23%     | 59.23%         |
| 64               | /26                |       84 |          482 | 12.50%     | 71.73%         |
| 128              | /25                |       80 |          562 | 11.90%     | 83.63%         |
| 256              | /24                |       62 |          624 | 9.23%      | 92.86%         |
| 512              | /23                |       31 |          655 | 4.61%      | 97.47%         |
| 1024             | /22                |       14 |          669 | 2.08%      | 99.55%         |
| >=2048           | >=/21              |        3 |          672 | 0.45%      | 100.00%        |
+------------------+--------------------+----------+--------------+------------+----------------+
(Table 2)
```
-->

Implications on lower bound of allocation
-----------------------------------------

Already today, more than 10% of the peering LANs are operated with a network smaller or equal a /25 (Figure 1). Roughly
83% of all IXPs would theoretically fit into a /25 (see Figure 2). Thus it makes sense to move to /25 assignments.
 
The current policy of assigning /24s by default has caused a lot of unused space as 74% of all peering LANs are operated 
with /24s (Figure 1), but the vast majority (83%) of IXPs cannot even utilize a /25 even when including 100% 
overprovisioning (Figure 2).

Implications on upper bound of allocation
-----------------------------------------

Large IXPs requiring a /23 or larger are very rare (<3%) (see Table 2). Thus, lowering the upper bound for assignments 
will not save large amounts of space. Large allocations should still be possible but should be thoroughly checked by 
RIPE. Due to the small number of large IXPs, the workload will obviously not be high for RIPE (Figure 1/2).
