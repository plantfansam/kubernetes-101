CLUSTER_SHORTHAND=$1
CLUSTER_ID=$(envchain do terraform output $CLUSTER_SHORTHAND)
OUTFILE="${CLUSTER_SHORTHAND}_config"
echo $CLUSTER_ID
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer ${TF_VAR_do_token}" "https://api.digitalocean.com/v2/kubernetes/clusters/$CLUSTER_ID/kubeconfig" > $OUTFILE

