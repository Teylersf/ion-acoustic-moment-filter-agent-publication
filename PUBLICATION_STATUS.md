# Publication observations

This is the authorized **Lattice Audit Agent** edition. **Taylor Kalin** remains the canonical author and human operator. Scientific text, the final payload and all 50 mixed-pin source copies remain unchanged.

## AgentPub

The first formal request returned HTTP 201 on 29 October 2026 at 23:49:09 UTC, assigning `paper_2026_dd331d`. An independent anonymous GET returned the complete stored paper with status **submitted**, no publication timestamp, and zero reviewer reports at the observation time.

- [Public paper page](https://agentpub.org/papers/paper_2026_dd331d)
- [Public stored JSON](https://api.agentpub.org/v1/papers/paper_2026_dd331d)
- [Independent stored-science verification](reproduction/agentpub-stored-science-verification.json)

All seven section text strings match the submitted payload exactly. Reversing the documented prose citation and figure-route adaptations restores all six original scientific bodies, 104 ordered mathematical segments, 13 equation tags, both complete figure/caption pairs and the full five-reference bibliography. All submitted reference fields remain intact. The service adds empty optional fields, extracted citation labels and display-style tags; these changes are enumerated in the verification receipt.

The public HTML endpoint returned HTTP 200 and contained the title and all seven headings. This verifies source availability only. Browser mathematical rendering, layout and a generated AgentPub PDF have not been inspected; the API's generated-file fields were null. The [complete canonical PDF](https://github.com/Teylersf/ion-acoustic-moment-filter-audit/releases/download/v1.0.0/main.pdf) remains the verified typeset fallback. Submission and public retrieval do not establish acceptance or completed peer review.

## Prior review and AAES

This study's own Publish.fun first round ended in a final rejection at 23:36:53 UTC on 29 October 2026, after all three reports and the editor decision completed. The gate was verified before the first AgentPub request. The [canonical review assessment](https://github.com/Teylersf/ion-acoustic-moment-filter-audit/blob/2fa810d40fd93d35cbd78a6a21ffca706ed27a51/submissions/publishfun-round1-independent-note.md) distinguishes the venue's significance judgment from evidence-access claims.

One AAES registration attempt returned HTTP 403 at 23:51:51 UTC with the upstream message “Could not verify GitHub account.” No registry paper ID was obtained. No retry was performed by this verifier. GitHub Discussions and a non-answerable `AAES-Review` category were configured separately; repository readiness does not establish successful AAES registration.

The adapter's original `submission-context.json` is a conservative historical observation made during offline preparation. Its bytes remain preserved with the original proofs. This status note records the later actual formal request and public retrieval; it does not alter historical certifications or authorize duplicate submissions.

## Dataset follow-up

The reviewer-mentioned Harvard Dataverse DOI `10.7910/DVN/V2BYYQ` is genuine and source-linked. Its only publicly released inventory file is an archival manuscript PDF; no separate fields, filter configuration or postprocessing program is listed. No dataset file was downloaded. See the [bounded primary-metadata assessment](https://github.com/Teylersf/ion-acoustic-moment-filter-audit/blob/260927c1217ab341a2e8fe2168b927ce6d873e28/audit/dataset-candidate-verification/ASSESSMENT.md). This inventory does not supply a quantitative reanalysis of the source's diagnostics.
