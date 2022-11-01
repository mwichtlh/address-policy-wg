import requests
import json
from os import path
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

####################################################################################
# This is an analysis of peering LANs and IXP member ASes from peeeringdb.         #
####################################################################################
# Author: Matthias Wichtlhuber, DE-CIX, matthias (dot) wichtlhuber (at) de-cix.net #
####################################################################################

# Get data from peeringDB (with caching)
url = "https://www.peeringdb.com/api/ixlan?depth=2"
if not path.exists("data.json"):
    data = json.loads(requests.get(url).text)
    json.dump(data, open("data.json", "w"))
else:
    data = json.load(open("data.json", "r"))
data = data["data"]

# Helper function to extract the data
def extract_values(obj, key):
    arr = []

    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key:
                    arr.append(v)
                elif isinstance(v, (dict, list)):
                    extract(v, arr, key)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

# Extract data
prefs = extract_values(data, "prefix")
asns = extract_values(data, "net_set")

# Clean data
prefs = [int(prefix.split("/")[1]) for prefix in prefs if not ":" in prefix]
asns = [len(net) for net in asns]

#####################################
# Distribution of Peering LAN sizes #
#####################################

# Do the plot
sns.distplot(prefs, bins=np.arange(19.5, 29.5, 1.0), kde=False)
plt.xticks(np.arange(20.0, 28.0, 1.0))
plt.title("Distribution of IPv4 peering LAN prefix size")
plt.text(19.5, 420, "Methodology:\n"
                    "- Peering LAN prefix sizes from\n"
                    "peeringdb.com (https://www.\n"
                    "peeringdb.com/api/ixlan?depth=2)\n"
                    "- Data as of Oct 26 2022\n"
                    "- Data set includes 1014 peering\nLAN prefixes from 951 IXPs",
                    horizontalalignment='left', size='x-small', color='black',
                    bbox=dict(facecolor='white', edgecolor='black', pad=5.0))
plt.annotate("~12.03% of all existing IXP\npeering LANs are smaller\nor equal /25.",
             xy=(25, 10), xytext=(26.5, 100), fontsize="small", arrowprops=dict(arrowstyle="->"),
             horizontalalignment='center')
plt.annotate("",
             xy=(26, 10), xytext=(26, 90), fontsize="small", arrowprops=dict(arrowstyle="->"),
             horizontalalignment='center')
plt.annotate("",
             xy=(27, 10), xytext=(26, 90), fontsize="small", arrowprops=dict(arrowstyle="->"),
             horizontalalignment='center')
plt.annotate("",
             xy=(28, 10), xytext=(26, 90), fontsize="small", arrowprops=dict(arrowstyle="->"),
             horizontalalignment='center')
plt.xlabel("prefix size")
plt.ylabel("# Peering LANs")
plt.tight_layout()
plt.savefig("peering_lan_prefix_size.png", dpi=100)
plt.show()
plt.clf()

# Do some math for a table showing the data
hist = np.histogram(prefs, bins=np.arange(min(prefs), max(prefs)+2.0, 1.0))
prefix_size = ["/%i" % p for p in hist[1][:-1]]
no_ixps_abs = hist[0]
no_ixps_abs_cum = np.cumsum(no_ixps_abs)
no_ixps_rel = ["%.2f%%" % (i * 100.0) for i in np.true_divide(no_ixps_abs, no_ixps_abs.sum())]
no_ixps_rel_cum = ["%.2f%%" % (i * 100.0) for i in np.true_divide(no_ixps_abs_cum, no_ixps_abs.sum())]
table_data = {"Prefix size": prefix_size,
              "# Peering LANs": no_ixps_abs,
              "# Peering LANs cum": no_ixps_abs_cum,
              "# Peering LANs rel": no_ixps_rel,
              "# Peering LANs rel cum": no_ixps_rel_cum
             }
print(tabulate(table_data, headers='keys', tablefmt='psql'))

#######################
# CDF of ASNs per IXP #
#######################

# Do the plot
asns_doubled = [a * 2 for a in asns]
ax = sns.distplot(asns_doubled, bins=range(1, max(asns_doubled), 1),
                  kde=False, hist_kws=dict(cumulative=True, density=True))
plt.annotate("82.02% of all IXPs would fit into a /25\nincluding 100% overprovisioning.",
             xy=(128, 0.83), xytext=(68, 0.6), fontsize="small", arrowprops=dict(arrowstyle="->"))
plt.annotate("71.71% of all IXPs would fit into a /26\nincluding 100% overprovisioning.",
             xy=(64, 0.71), xytext=(17, 0.9), fontsize="small", arrowprops=dict(arrowstyle="->"))
plt.annotate("<4% of all IXPs require /23 or larger\nincluding 100% overprovisioning.",
             xy=(512, 0.97), xytext=(260, 0.8), fontsize="small", arrowprops=dict(arrowstyle="->"))
plt.text(128, 0.1, "Methodology:\n"
                   "- AS set sizes from peeringdb.com\n(https://www.peeringdb.com/api/ixlan?depth=2)\n"
                   "- Data as of Oct 26 2022\n"
                   "- Data set includes 951 IXPs\n"
                   "- Required IPs is assumed to be twice the size of IXP's AS set\n"
                   "- Note logarithmic x axis",
                   horizontalalignment='left', size='x-small', color='black',
                   bbox=dict(facecolor='white', edgecolor='black', pad=5.0))
plt.xlim([16, max(asns_doubled)-1])
plt.ylim([0.0, 1.001])
plt.xscale("log", basex=2)
plt.title("CDF of required IPs per IXP")
plt.xlabel("# required IPs\n(=2xASes/IXP, i.e., including 100% overprovisioning)")
plt.ylabel("IXPs with less than x required IPs [%] (CDF)")
xticks = [pow(2, x) for x in range(3, 12)]
xtick_labels = ["%i\n(/%i)" % (pow(2, x), 32-x) for x in range(3, 12)]
plt.xticks(xticks, xtick_labels)
for i in [pow(2, x) for x in range(3, 12)]:
    plt.axvline(i, linestyle="--", color="k", linewidth=0.5)
plt.yticks(np.arange(0.0, 1.1, 0.1), np.arange(0, 110, 10))
plt.tight_layout()
plt.savefig("required_ips_per_ixp.png", dpi=100)
plt.show()

# Do some math for a table showing the data
xticks.insert(0, 1)
hist = np.histogram(asns_doubled, bins=xticks)

# Format the data
sizes = hist[1][1:]
pref_sizes = [int(32 - np.log2(x)) for x in sizes]
pref_sizes = ["/%i" % s for s in pref_sizes]
pref_sizes[0] = "<%s" % pref_sizes[0]
pref_sizes[-1] = ">=%s" % pref_sizes[-1]
sizes = ["%i" % s for s in sizes]
sizes[0] = "<%s" % sizes[0]
sizes[-1] = ">=%s" % sizes[-1]
peers_abs = hist[0]
peers_abs_cum = np.cumsum(peers_abs)
peers_rel = ["%.2f%%" % (i * 100.0) for i in np.true_divide(peers_abs, peers_abs.sum())]
peers_rel_cum = ["%.2f%%" % (i * 100.0) for i in np.true_divide(peers_abs_cum, peers_abs.sum())]

# Create and print a table
table_data = {
    "# req. IPs/IXP": sizes,
    "min. prefix size": pref_sizes,
    "# IXPs": peers_abs,
    "# IXPs cum": peers_abs_cum,
    "IXPs rel": peers_rel,
    "IXPs rel cum": peers_rel_cum
}
print(tabulate(table_data, headers='keys', tablefmt='psql'))
