WITH leg_view AS (

    /* =========================
       INBOUND LEGS
       ========================= */
    SELECT
        i.interact_uuid_id,
        i.interact_seg_uuid_id,
        i.interact_seg_seq_no,
        i.recover_key_id,
        i.guid,
        i.precision_queue_nm,
        'INBOUND' AS leg_direction,
        i.prev_seg_transfer,
        NULL AS call_meth_nm,
        NULL AS inbd_interact_seg_uuid_id
    FROM inbound i

    UNION ALL

    /* =========================
       OUTBOUND LEGS
       ========================= */
    SELECT
        o.interact_uuid_id,
        o.interact_seg_uuid_id,
        o.interact_seg_seq_no,
        o.recover_key_id,
        NULL AS guid,
        o.precision_queue_nm,
        'OUTBOUND' AS leg_direction,
        NULL AS prev_seg_transfer,
        o.call_meth_nm,
        o.inbd_interact_seg_uuid_id
    FROM outbound o
),

consult_graph AS (

    /* =========================
       CONSULT / WARM TRANSFER GRAPH
       (third person entered)
       ========================= */
    SELECT
        o.interact_uuid_id,

        /* source inbound leg */
        src.interact_seg_uuid_id AS src_seg_uuid,
        src.guid                 AS src_guid,
        src.precision_queue_nm   AS src_precision,
        src.interact_seg_seq_no  AS src_seq,

        /* consult outbound leg */
        o.interact_seg_uuid_id   AS consult_seg_uuid,
        o.interact_seg_seq_no    AS consult_seq,

        /* destination inbound leg */
        dst.interact_seg_uuid_id AS dst_seg_uuid,
        dst.guid                 AS dst_guid,
        dst.precision_queue_nm   AS dst_precision,
        dst.interact_seg_seq_no  AS dst_seq

    FROM leg_view o

    /* outbound consult / warm leg */
    JOIN leg_view src
      ON src.interact_seg_uuid_id = o.inbd_interact_seg_uuid_id
     AND src.leg_direction = 'INBOUND'

    JOIN leg_view dst
      ON dst.interact_uuid_id = o.interact_uuid_id
     AND dst.leg_direction = 'INBOUND'
    --  If your system sometimes skips seq_no + 1, replace that join with:
    --  AND dst.interact_seg_seq_no > o.interact_seg_seq_no
     AND dst.interact_seg_seq_no = o.interact_seg_seq_no + 1

    WHERE o.leg_direction = 'OUTBOUND'
      AND o.call_meth_nm IN ('CONSULT', 'WARM_TRANSFER')
)

SELECT DISTINCT
    cg.interact_uuid_id,
    cg.src_guid,
    cg.dst_guid,
    cg.src_precision,
    cg.dst_precision,
    it.init_precision_queue_nm,
    it.finl_precision_queue_nm

FROM consult_graph cg

JOIN interact it
  ON it.interact_uuid_id = cg.interact_uuid_id

WHERE
    (
        it.init_precision_queue_nm LIKE '%PATTERN1%'
        OR it.init_precision_queue_nm LIKE '%PATTERN2%'
        OR it.init_precision_queue_nm LIKE '%PATTERN3%'
        OR it.finl_precision_queue_nm LIKE '%PATTERN1%'
        OR it.finl_precision_queue_nm LIKE '%PATTERN2%'
        OR it.finl_precision_queue_nm LIKE '%PATTERN3%'
    );
