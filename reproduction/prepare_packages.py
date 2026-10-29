"""Offline agent-edition adapter. No network, Git, credentials or submission.

Requires byte-pinned bundled inputs and an explicit private outgoing directory.
Only agent front matter, figure routes, platform grouping and reversible prose
citation formatting change; scientific text is never shortened or padded.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_REPOSITORY = "https://github.com/Teylersf/ion-acoustic-moment-filter-audit"
AGENT_REPOSITORY = "https://github.com/Teylersf/ion-acoustic-moment-filter-agent-publication"
AGENT_NAME = "Lattice Audit Agent"
AGENT_ID = "agent_29b9bf7a"
IDENTITY = "gist:7c74312cf47dcc31c789a8b1c3dedd25"
HEADINGS = ["Introduction", "Related Work", "Methodology", "Results", "Discussion", "Limitations", "Conclusion"]
TAGS = ["magnetic-reconnection", "ion-acoustic-instability", "moment-closure", "spatial-filtering", "reproducibility"]
MATH = re.compile(r"\\\[.*?\\\]|\\\(.*?\\\)|\$\$.*?\$\$|(?<![\\$])\$(?!\$).*?(?<!\\)\$(?!\$)", re.S)
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
SCRIPT_BYTES = Path(__file__).read_bytes()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")

def words(text):
    return len(re.findall(r"\b[\w'-]+\b", text))

def section_map(text):
    matches = list(re.finditer(r"^## (.+)$", text, re.M))
    result = {}
    for i, match in enumerate(matches):
        if match[1] in result:
            raise ValueError("Duplicate canonical top-level section")
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        result[match[1]] = text[match.end():end].strip()
    return result

def scientific_sections(parsed):
    numbered = [(h, b) for h, b in parsed.items() if re.fullmatch(r"[1-6]\. .+", h)]
    if [int(h.split(".", 1)[0]) for h, _ in numbered] != list(range(1, 7)):
        raise ValueError("Expected exactly canonical scientific sections 1 through 6")
    if list(parsed) != ["Abstract", *(h for h, _ in numbered), "References"]:
        raise ValueError("Unrecognized, reordered or omitted top-level section; no appendix is expected")
    return numbered

def protected(text):
    return {
        "math": MATH.findall(text),
        "tables": re.findall(r"(?m)^(?:[ \t]*\|[^\n]*\|[ \t]*(?:\n|$))+", text),
        "quotations": re.findall(r"(?m)^(?:>[^\n]*(?:\n|$))+", text),
        "code_fences": re.findall(r"(?ms)^```[^\n]*\n.*?^```[ \t]*$", text),
        "proof_markers": re.findall(r"(?m)^(?:#{3,6}\s+)?(?:\*\*)?Proof\b[^\n]*", text),
        "figures": IMAGE.findall(text),
    }

def paragraphs(text):
    return Counter(block.strip() for block in re.split(r"\n\s*\n", text.strip())
                   if block.strip() and not re.fullmatch(r"#{1,6} .+", block.strip()))

def reference_records(text):
    matches = list(re.finditer(r"^\[(\d+)\] (.+?)(?=\n\n\[\d+\] |\Z)", text, re.M | re.S))
    refs, originals = [], []
    for match in matches:
        number, record = match[1], match[2].strip()
        originals.append(match[0].strip())
        title = re.search(r"(?<!\*)\*([^*]+)\*(?!\*)", record)
        if title is None:
            raise ValueError("A verified explicit reference title is required")
        authors = [part.strip() for part in re.split(r",\s*|\s+and\s+", record[:title.start()].rstrip(", ")) if part.strip()]
        urls = [url.rstrip(".;,") for url in re.findall(r"https?://[^\s]+", record)]
        years = re.findall(r"\b(?:19|20)\d{2}\b", record)
        if not authors or not urls or not years:
            raise ValueError("Reference lacks canonical authors, URL or year")
        ref = {"ref_id": number, "type": "external", "title": title[1],
               "authors": authors, "year": int(years[0]), "url": urls[0],
               "source": "arxiv" if "arxiv.org" in urls[0] else "doi" if "doi.org/" in urls[0] else "url"}
        doi = next((url.split("doi.org/", 1)[1] for url in urls if "doi.org/" in url), None)
        if doi:
            ref["doi"] = doi
        refs.append(ref)
    if [int(ref["ref_id"]) for ref in refs] != list(range(1, len(refs) + 1)):
        raise ValueError("Noncontiguous or missing bibliography")
    if "\n\n".join(originals) != text:
        raise ValueError("Reference parser failed to preserve all canonical records")
    return refs, originals

def author_year_citations(text, references):
    """Reformat prose markers reversibly; mathematics and code stay exact."""
    labels = {"1": "Li, Liu and Loureiro, 2026", "2": "Li, Liu and Loureiro, 2025",
              "3": "Savitzky and Golay, 1964", "4": "Germano, 1992",
              "5": "Kalin, 2026"}
    if {r["ref_id"] for r in references} != set(labels):
        raise ValueError("Review author-year map against the complete bibliography")
    protected_spans = [(m.start(), m.end()) for m in MATH.finditer(text)]
    for pattern in [r"(?ms)^```[^\n]*\n.*?^```[ \t]*$", r"`[^`\n]+`"]:
        protected_spans.extend((m.start(), m.end()) for m in re.finditer(pattern, text))
    pattern = re.compile(r"\[([0-9]+(?:\s*,\s*[0-9]+)*)(,\s*[A-Za-z][^\]]*)?\](?!\()")
    parts, ledger, cursor, length = [], [], 0, 0
    for match in pattern.finditer(text):
        if any(match.start() < end and match.end() > start for start, end in protected_spans):
            continue
        ids = [x.strip() for x in match[1].split(",")]
        if any(x not in labels for x in ids):
            raise ValueError("Unresolved prose reference marker")
        prefix = text[cursor:match.start()]
        parts.append(prefix); length += len(prefix)
        rewritten = "[" + "; ".join(labels[x] for x in ids) + (match[2] or "") + "]"
        ledger.append({"canonical": match[0], "adapted": rewritten,
                       "reference_ids": ids, "adapted_start": length,
                       "adapted_end": length + len(rewritten)})
        parts.append(rewritten); length += len(rewritten); cursor = match.end()
    parts.append(text[cursor:])
    converted = "".join(parts)
    if restore_citations(converted, ledger) != text:
        raise ValueError("Author-year transformation is not exactly reversible")
    return converted, ledger

def restore_citations(text, ledger):
    for row in reversed(ledger):
        start, end = row["adapted_start"], row["adapted_end"]
        if text[start:end] != row["adapted"]:
            raise ValueError("Citation reversal locator or text changed")
        text = text[:start] + row["canonical"] + text[end:]
    return text


def safe(name, data):
    """Do not leak local paths, credentials or operational state into outputs."""
    path = Path(name)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Unsafe package route")
    if not name.lower().endswith((".png", ".pdf")):
        text = data.decode("utf-8")
        # This generic reproduction runtime is intentionally public in H.
        scrubbed = text.replace("C:/Python313/python.exe", "PYTHON")
        scrubbed = scrubbed.replace("C:\\Python313\\python.exe", "PYTHON")
        if name == "reproduction/canonical/.gitignore":
            scrubbed = scrubbed.replace(".publishing-access/", "PRIVATE_IGNORE_PATTERN/")
        if re.search(r"(?i)(?:(?<![A-Z0-9])[A-Z]:[\\/]|/mnt/[a-z]/|/home/|/root/|\.publishing-access)", scrubbed):
            raise ValueError("Private location in public file: " + name)
        if re.search(r"(?i)(?:Bearer\s+[A-Za-z0-9._-]{12,}|(?:session_token|access_token|api_key)\s*[=:]\s*[\"']?[A-Za-z0-9._-]{12,}|gh[pousr]_[A-Za-z0-9]{20,})", text):
            raise ValueError("Credential-shaped value in public file: " + name)


def inputs(args):
    raw = (ROOT / "reproduction/pinned-inputs.json").read_bytes()
    if sha(raw) != args.expected_input_inventory_sha256:
        raise ValueError("Mixed-pin input inventory changed")
    inventory = json.loads(raw)
    for key, value in {
        "computational_commit": args.expected_code_commit,
        "computational_tree": args.expected_code_tree,
        "canonical_content_commit": args.canonical_content_commit,
        "computational_file_count": 42, "paper_support_file_count": 8,
        "file_count": 50,
    }.items():
        if inventory.get(key) != value:
            raise ValueError("Input inventory mismatch: " + key)
    rows = inventory["files"]
    if len(rows) != 50 or len({r["package_path"] for r in rows}) != 50:
        raise ValueError("Missing or duplicate copied files")
    copies = {}
    roles = Counter()
    for row in rows:
        route = row["package_path"]
        if route != "reproduction/canonical/" + row["source_path"]:
            raise ValueError("Unexpected copy route")
        data = (ROOT / route).read_bytes()
        if len(data) != row["bytes"] or sha(data) != row["sha256"]:
            raise ValueError("Pinned bytes differ: " + route)
        role = row["role"]
        expected = args.expected_code_commit if role == "immutable_computational_snapshot" else args.canonical_content_commit
        if row["source_revision"] != expected:
            raise ValueError("Wrong source revision")
        safe(route, data)
        copies[route] = data
        roles[role] += 1
    if roles != Counter({"immutable_computational_snapshot": 42, "canonical_paper_TeX_builder_metadata": 8}):
        raise ValueError("Wrong source scopes")
    comp = {r["source_path"]: r for r in rows if r["role"] == "immutable_computational_snapshot"}
    manifest = json.loads(copies["reproduction/canonical/data/computational-artifact-manifest.json"])
    records = manifest["files"]
    if set(comp) != {r["path"] for r in records} | {"data/computational-artifact-manifest.json"}:
        raise ValueError("Incomplete frozen computational manifest")
    for row in records:
        if comp[row["path"]]["sha256"] != row["sha256"]:
            raise ValueError("Frozen manifest byte mismatch")
    return copies, inventory, raw


def arrangement(numbered):
    first = numbered[0][1].split("\n\n")
    if len(first) != 4:
        raise ValueError("Review section 1 boundaries")
    ending = numbered[5][1]
    anchor = "A focused revision could remove the zero-divisor inference"
    if ending.count(anchor) != 1:
        raise ValueError("Review limitations/conclusion boundary")
    pos = ending.index(anchor)
    added = ["### " + numbered[i][0] for i in (1, 2, 3)]
    bodies = [first[0], first[1],
              "\n\n".join(first[2:]) + "\n\n" + added[0] + "\n\n" + numbered[1][1],
              added[1] + "\n\n" + numbered[2][1] + "\n\n" + added[2] + "\n\n" + numbered[3][1],
              numbered[4][1], ending[:pos].strip(), ending[pos:].strip()]
    if any(not body for body in bodies):
        raise ValueError("Empty platform group")
    return bodies, added


def main():
    if sys.flags.optimize:
        raise RuntimeError("Ordinary Python required; -O disables preservation assertions")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outgoing-dir", type=Path, required=True)
    for name in ("expected-code-commit", "expected-code-tree", "canonical-content-commit",
                 "expected-manuscript-sha256", "expected-pdf-sha256", "expected-input-inventory-sha256"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    outgoing = args.outgoing_dir.resolve()
    canonical = ROOT.parent / "ion-acoustic-moment-filter-audit"
    if outgoing.is_relative_to(ROOT) or outgoing.is_relative_to(canonical):
        raise ValueError("Outgoing API bodies must stay outside both repositories")
    for value in (args.expected_code_commit, args.expected_code_tree, args.canonical_content_commit):
        if not re.fullmatch(r"[a-f0-9]{40}", value):
            raise ValueError("Full source commit/tree pins required")
    for value in (args.expected_manuscript_sha256, args.expected_pdf_sha256, args.expected_input_inventory_sha256):
        if not re.fullmatch(r"[a-f0-9]{64}", value):
            raise ValueError("Full SHA256 required")
    if args.expected_code_commit == args.expected_code_tree:
        raise ValueError("Commit and tree are distinct objects")
    source, inventory, inventory_raw = inputs(args)
    md = source["reproduction/canonical/paper/manuscript.md"]
    pdf = source["reproduction/canonical/paper/main.pdf"]
    if sha(md) != args.expected_manuscript_sha256 or sha(pdf) != args.expected_pdf_sha256:
        raise ValueError("Paper content pins changed")
    text = md.decode("utf-8")
    if "\r" in text:
        raise ValueError("Canonical LF must stay exact")
    parsed = section_map(text)
    numbered = scientific_sections(parsed)
    science = "\n\n".join(body for _, body in numbered)
    title = re.search(r"^# (.+)$", text, re.M)[1]
    version, date = re.search(r"^Version ([^;\s]+); (.+)$", text, re.M).groups()
    meta_raw = source["reproduction/canonical/submissions/metadata.json"]
    meta = json.loads(meta_raw)
    for key, expected in {"title": title, "abstract": parsed["Abstract"], "author": "Taylor Kalin",
                          "version": "1.0.0", "scientific_code_commit": args.expected_code_commit,
                          "repository": CANONICAL_REPOSITORY, "agentpub_paper_type": "short_communication"}.items():
        if meta.get(key) != expected:
            raise ValueError("Canonical metadata changed: " + key)
    assert "**Taylor Kalin**" in text.split("## Abstract", 1)[0]
    assert args.expected_code_commit in science and "https://doi.org/" + meta["code_doi"] in science
    references, original_refs = reference_records(parsed["References"])
    assert len(references) == 5
    image_routes = {}
    for _, link in IMAGE.findall(science):
        if not re.fullmatch(r"\.\./figures/[a-z-]+\.png", link):
            raise ValueError("Unrecognized figure route")
        filename = link.rsplit("/", 1)[1]
        local = "reproduction/canonical/figures/" + filename
        if local not in source:
            raise ValueError("Figure not pinned")
        remote = "https://raw.githubusercontent.com/Teylersf/ion-acoustic-moment-filter-audit/" + args.expected_code_commit + "/figures/" + filename
        image_routes[link] = (local, remote)
    assert len(image_routes) == 2

    def adapt(body, remote=False):
        for old, pair in image_routes.items():
            body = body.replace("](" + old + ")", "](" + pair[int(remote)] + ")")
        return body

    def restore(body, remote=False):
        for old, pair in image_routes.items():
            body = body.replace("](" + pair[int(remote)] + ")", "](" + old + ")")
        return body

    front = ("# " + title + "\n\n**" + AGENT_NAME + "**\n\n"
             "Authorized agent-only edition. Human operator and canonical author: **Taylor Kalin**.\n\n"
             "AgentPub identity: `" + AGENT_ID + "`; AAES identity: `" + IDENTITY + "`.\n\n"
             "Canonical author: https://taylorkalin.com ; ORCID 0009-0003-9000-9315.\n\n"
             "Version " + version + "; " + date + "\n\n"
             "**Agent-edition disclosure.** All scientific paragraphs, mathematics, equations, derivations, figures, captions, references and original disclosures are retained. "
             "This front byline/disclosure and figure routes are adapted. AgentPub alone additionally groups paragraphs into venue sections and uses reversible documented author-year prose citations. "
             "The canonical author remains Taylor Kalin. Internal AI-assisted checks are not independent human peer review.\n\n")
    paper = front + "## Abstract\n\n" + parsed["Abstract"] + "\n\n" + "\n\n".join(
        "## " + h + "\n\n" + adapt(body) for h, body in numbered) + "\n\n## References\n\n" + parsed["References"] + "\n"
    grouped, added = arrangement(numbered)
    sections, ledgers = [], {}
    for heading, body in zip(HEADINGS, grouped):
        content, ledger = author_year_citations(adapt(body, True), references)
        ledgers[heading] = ledger
        sections.append({"heading": heading, "content": content,
                         "citations": sorted({r for row in ledger for r in row["reference_ids"]}, key=int)})
    restored = "\n\n".join(restore(restore_citations(s["content"], ledgers[s["heading"]]), True) for s in sections)
    for heading in added:
        if restored.count(heading + "\n\n") != 1:
            raise ValueError("Added source heading changed")
        restored = restored.replace(heading + "\n\n", "", 1)
    local = section_map(paper)
    restored_local = "\n\n".join(restore(b) for _, b in scientific_sections(local))
    assert restored == restored_local == science
    assert paragraphs(restored) == paragraphs(science)
    assert protected(restored) == protected(restored_local) == protected(science)
    assert local["Abstract"] == parsed["Abstract"] and local["References"] == parsed["References"]
    tags = re.findall(r"\\tag\{([^{}]+)\}", science)
    assert tags == list(map(str, range(1, 14)))
    schema_raw = (ROOT / "reproduction/agentpub-paper-schema.json").read_bytes()
    limits = json.loads(schema_raw)["paper_types"]["short_communication"]["constraints"]
    caps = {s["heading"]: {"unicode_codepoints": len(s["content"]),
                           "UTF16_code_units": len(s["content"].encode("utf-16-le")) // 2} for s in sections}
    body_words = sum(words(s["content"]) for s in sections)
    guideline_checks = {
        "title": len(title) <= limits["title"]["max_chars"],
        "abstract": words(parsed["Abstract"]) <= limits["abstract"]["max_words"],
        "references": len(references) >= limits["references"]["min_count"],
        "body_words": limits["body_word_count"]["min_words"] <= body_words <= limits["body_word_count"]["max_words"],
        "required_sections": set(limits["sections"]["required"]) <= set(HEADINGS),
        "section_order": [h for h in limits["sections"]["must_appear_in_this_order"] if h in HEADINGS] == HEADINGS,
        "section_character_caps": all(max(c.values()) <= 49000 for c in caps.values()),
        "tags": limits["tags"]["min_count"] <= len(TAGS) <= limits["tags"]["max_count"] and all(len(t) <= limits["tags"]["max_chars_each"] for t in TAGS),
    }
    if not all(guideline_checks.values()):
        raise ValueError("Selected live paper-type constraints failed: " + str(guideline_checks))
    note = ("Authorized agent-only edition by Lattice Audit Agent; human operator and canonical author Taylor Kalin, ORCID 0009-0003-9000-9315. "
            "Canonical: " + CANONICAL_REPOSITORY + "/blob/" + args.canonical_content_commit + "/paper/manuscript.md . "
            "Six original sections map losslessly into seven venue groups at paragraph boundaries, in original scientific order; three exact source subheadings are added. "
            "All scientific text, ordered mathematics, equations, derivations, original figures/captions, bibliography and disclosures remain after reversing declared figure routes and author-year substitutions. "
            "AgentPub prose uses [Author, Year] as documented at https://api.agentpub.org/v1/instructions; local paper keeps exact numeric citations. "
            "Li, Liu and Loureiro 2026 denotes reference 1 (final journal); Li, Liu and Loureiro 2025 denotes reference 2 (arXiv v1). Citations arrays retain numeric reference IDs. "
            "No scientific shortening or padding. Exact model/token usage was not recorded; agent_model='not recorded' and total_tokens=-1 expressly denote missing data, not estimates. "
            "No new PIC/kinetic simulation, recovered source postprocessing implementation or independent human peer review is claimed. The source's actual window-centered convention could already satisfy the covariance identity. "
            "Two complete inline Markdown figure/caption pairs link directly to the immutable public computational snapshot; no unsupported structured-image data keys are guessed. "
            "Complete typeset canonical PDF: " + CANONICAL_REPOSITORY + "/releases/download/v1.0.0/main.pdf . "
            "Formal agent submission requires this study's own final Publish.fun release/closure; offline preparation and nonstoring validation do not open that gate. "
            "Full canonical bibliography follows verbatim; normalized reference fields alone omit page/version/inspection qualifiers.\n\n" + parsed["References"])
    payload = {"title": title, "abstract": parsed["Abstract"], "paper_type": "short_communication",
               "authors": [{"agent_id": AGENT_ID, "display_name": AGENT_NAME, "model_type": "not recorded"}],
               "sections": sections, "references": references, "tags": TAGS,
               "metadata": {"agent_model": "not recorded", "agent_platform": "Codex desktop", "total_tokens": -1, "submission_note": note}}
    now = datetime.now(timezone.utc).isoformat()
    context = {"prepared_at_utc": now, "publication_state": "local_prepared_not_submitted", "canonical_version": version,
               "computational_commit": args.expected_code_commit, "computational_tree": args.expected_code_tree,
               "canonical_content_commit": args.canonical_content_commit, "canonical_manuscript_sha256": sha(md),
               "AgentPub_submission_gate_open": False, "AAES_submission_gate_open": False,
               "own_Publishfun_final_disposition_verified": False, "formal_submission_performed": False,
               "public_agent_repository_verified": False,
               "note": "Conservative offline state. Root owns the first Publish.fun submission and live disposition. A preflight never opens a formal gate. No acceptance, closure, release or agent eligibility is inferred."}
    metadata = {"aaes_version": "4.2", "title": title, "abstract": parsed["Abstract"], "canonical_version": version,
                "author_ids": [IDENTITY], "submitted_at": now, "timestamp_scope": "local preparation, not registration",
                "tags": TAGS, "agentpub_paper_type": "short_communication",
                "computational_commit": args.expected_code_commit, "computational_tree": args.expected_code_tree,
                "canonical_content_commit": args.canonical_content_commit,
                "generation_environment": {"model": "not recorded", "tools": ["Python", "exact rational arithmetic", "NumPy", "Matplotlib"],
                    "prompt_strategy": "Read both source editions fully; check continuity without division, restrict literal density conventions, verify finite-filter identities with exact controls and retain contrary interpretations.",
                    "notes": "Agent Lattice Audit Agent; human operator/canonical author Taylor Kalin. Self-funded. No estimated model/token usage or independent human peer review."},
                "novelty_statement": "Source-specific consistency analysis of a singular moment reduction and finite spatial averaging conventions; standard continuity/covariance identities are not new plasma theory. No recovered original postprocessing, changed plotted amplitude or revised reconnection rate is established."}
    claims = [
        {"text": "Steady continuity at a positive-density stagnation point sets the divisor in the source temperature relation to zero.", "kind": "finding", "status": "proposed", "evidence_summary": "Section 2, Eqs. (1)-(5); literal moment elimination explicitly restricted to n=m=e=1.", "confidence_note": "Underdetermined moment subsystem; no claim that the observed heating or temperature scale is impossible."},
        {"text": "Finite spatial covariance generally differs from filtering the product of pointwise residuals.", "kind": "finding", "status": "proposed", "evidence_summary": "Sections 3-4; exact rational signed Savitzky-Golay examples and cross terms.", "confidence_note": "No original postprocessing implementation or underlying source fields were obtained."},
        {"text": "Centering both fields by the same window-center means exactly recovers covariance, including signed filter weights.", "kind": "finding", "status": "proposed", "evidence_summary": "Section 4, Eq. (11); exact 4-kernel controls.", "confidence_note": "The source authors may already use this valid convention; no plotted anomaly is demonstrated."},
        {"text": "The public controls verify 273 normalized states and 20 filter cases with 40 signed-charge temporal controls.", "kind": "finding", "status": "proposed", "evidence_summary": "Section 5 and immutable code archive; 266 finite-divergence paths intentionally violate exact steady continuity and seven zero-divergence endpoints remain underdetermined.", "confidence_note": "Synthetic exact algebra, not full kinetic or new PIC reconnection simulations."},
        {"text": "Final-edition Doppler changes and the universal Appendix E scale interpretation remain positive controls.", "kind": "finding", "status": "proposed", "evidence_summary": "Sections 1 and 5; explicit withdrawal of an earlier threshold candidate.", "confidence_note": "No source instability/heating observation is refuted; applicability and extrapolation qualifiers remain."},
    ]
    registration = {"source": "github:Teylersf/ion-acoustic-moment-filter-agent-publication",
                    "submission": {"kind": "paper", "maturity": "final"},
                    "project": {"title": title, "summary": parsed["Abstract"], "status": "active",
                                "research_question": "Are the moment division and finite-filter fluctuation conventions sufficient to support the stated analytical diagnostics?"},
                    "claims": claims}
    blocks = protected(science)
    checks = {"prepared_at_utc": now, "canonical_version": version,
              "preparer_sha256": sha(SCRIPT_BYTES), "pinned_input_inventory_sha256": sha(inventory_raw),
              "canonical_manuscript_sha256": sha(md), "canonical_PDF_sha256": sha(pdf), "canonical_metadata_sha256": sha(meta_raw),
              "computational_commit": args.expected_code_commit, "computational_tree": args.expected_code_tree,
              "canonical_content_commit": args.canonical_content_commit, "code_doi": meta["code_doi"],
              "copied_pinned_files": inventory["files"], "copy_counts": {"computational_H": 42, "paper_TeX_builder_metadata_release": 8, "total": 50},
              "canonical_scientific_sections": 6, "platform_sections": HEADINGS,
              "mapping": "Original scientific order; section 1 paragraphs 1/2/3-4 become Intro/Related Work/Methods; Methods also contains section 2; Results sections 3-4; Discussion section 5; section 6 split at recorded paragraph boundary.",
              "added_platform_headings": added,
              "full_scientific_text_exact_after_declared_reversal": True, "ordered_paragraphs_and_protected_blocks_preserved": True,
              "abstract_and_full_bibliography_exact": True, "canonical_bibliography_verbatim_in_payload_metadata": True,
              "math_segments": len(blocks["math"]), "protected_block_counts": {k: len(v) for k, v in blocks.items()},
              "numbered_equation_tags": tags, "figures": len(image_routes), "references": len(references),
              "scientific_section_bodies": [{"heading": h, "sha256": sha(b.encode())} for h, b in numbered],
              "citation_format": {"documented_style": "[Author, Year]", "instructions_URL": "https://api.agentpub.org/v1/instructions",
                  "reversal_ledger_by_section": ledgers, "local_numeric_markers_unchanged": True, "math_code_link_labels_excluded": True},
              "figure_interface": {"inline_Markdown_pairs_preserved": 2, "structured_figures_submitted": 0,
                  "note": "Live schema declares optional figures[].data as an unspecified object; no image-data keys are invented. The full PDF is the typeset fallback, separately from API-text preservation."},
              "section_character_counts": caps, "body_regex_words": body_words,
              "body_whitespace_words": sum(len(s["content"].split()) for s in sections), "guideline_checks": guideline_checks,
              "paper_type": "short_communication", "schema_snapshot_sha256": sha(schema_raw),
              "agentpub_payload_sha256": sha(encode(payload)), "AAES_registration_sha256": sha(encode(registration)),
              "AAES_bounded_claims": len(claims), "model_or_token_usage_estimated": False, "unknown_token_sentinel": -1,
              "formal_agent_gates_open": False, "canonical_inputs_unchanged": True,
              "permitted_changes": ["agent front byline/disclosure", "figure routes", "lossless paragraph grouping and three source headings", "AgentPub-only reversible author-year prose markers"],
              "nonprivate_runtime_locator_allowlist": ["C:/Python313/python.exe"]}
    readme = f"""# {title}

Agent edition by **{AGENT_NAME}**. Human operator and canonical author: **Taylor Kalin**.

Version {version}. The [canonical paper]({CANONICAL_REPOSITORY}/blob/{args.canonical_content_commit}/paper/manuscript.md) retains Taylor's authorship. Every scientific paragraph, ordered mathematical block, derivation, figure, complete caption, reference and original disclosure is preserved. The lossless platform grouping and reversible author-year prose citation ledger are documented in [the preservation receipt](reproduction/adapter-checks.json).

- [Agent manuscript](paper.md)
- [Agent identity metadata](metadata.json)
- [Reproduction and mixed-pin inventory](reproduction/README.md)
- [Conservative submission context](reproduction/submission-context.json)
- [Complete typeset canonical PDF]({CANONICAL_REPOSITORY}/releases/download/v1.0.0/main.pdf)

The scoped findings concern division by zero in a normalized moment subsystem and the conventions needed for finite spatial covariance. They do not establish a new source temperature, a wrong plotted anomalous amplitude, a changed reconnection rate or a failed physical instability. The source's actual window-centered convention could already be valid. The withdrawn Appendix E candidate remains withdrawn. All stated source limitations and retained controls remain in the text.

This package preserves {len(blocks['math'])} mathematical segments, {len(tags)} numbered equations, {len(blocks['tables'])} Markdown tables, two figure/caption pairs and five references. It contains **42 exact computational files** at commit `{args.expected_code_commit}` (distinct tree `{args.expected_code_tree}`), and **8 exact paper/TeX/builder/metadata files** at `{args.canonical_content_commit}`. Public review components already belonging to the frozen computational archive are intentionally retained. Per-file revisions/hashes are in reproduction/pinned-inputs.json. The software DOI is https://doi.org/{meta['code_doi']}.

AgentPub uses its documented short_communication type and author-year prose references; this local paper retains the numeric bibliography and markers. No scientific shortening or citation padding is used. Two original inline Markdown image/caption pairs are retained. A viewer may render mathematics in tables or images differently from stored text; the complete PDF is the typeset fallback. No unsupported structured-figure keys or raw HTML are introduced.

**Prepared offline; not formally submitted.** This study's own final Publish.fun disposition has not been verified by the preparer. Both agent submission gates remain closed. Nonstoring validation is not submission, acceptance, identity eligibility, repository publication or a final review outcome. Exact model/token usage was not recorded; the explicit -1 token sentinel means missing data, not an estimate. Internal AI-assisted checks are not independent human peer review.

Own code: MIT. Own text/figures: CC BY 4.0. Attributed works retain their rights. Authorized agent identity: [{IDENTITY}](https://gist.github.com/Teylersf/7c74312cf47dcc31c789a8b1c3dedd25).
"""
    command = ("python reproduction/prepare_packages.py --outgoing-dir OUTSIDE_PUBLIC_REPOS "
               "--expected-code-commit " + args.expected_code_commit + " --expected-code-tree " + args.expected_code_tree +
               " --canonical-content-commit " + args.canonical_content_commit +
               " --expected-manuscript-sha256 " + sha(md) + " --expected-pdf-sha256 " + sha(pdf) +
               " --expected-input-inventory-sha256 " + sha(inventory_raw))
    reproduction = f"""# Reproduction and preservation

All 50 mixed-pin source blobs are bundled under canonical/. Run the offline adapter from the agent repository root with ordinary Python 3. It needs no Git, credentials, source PDF, network access, plotting dependencies or external canonical checkout. Outgoing bodies must be explicitly placed outside both public repositories.

```text
{command}
```

The adapter validates inventory sizes/SHA256, exact 42-file computational-manifest coverage, distinct commit/tree identities, paper/metadata pins and all protected scientific content before writing outputs. It rejects Python -O. It never launches simulations, contacts a venue, opens a gate or changes the canonical checkout. To rerun the scientific controls, follow canonical/REPRODUCIBILITY.md and canonical/COMPUTATIONAL_METHODS.md; exact rational verifiers use ordinary Python, while figure reproduction has the separately documented NumPy/Matplotlib requirements.

The six original scientific sections become seven AgentPub sections at paragraph boundaries, preserving their complete text in original order. Only three source headings, figure routes and documented author-year prose citations are adapted. The exact reversal ledger, every ordered mathematical block, all 13 equation tags, full bibliography and both captions are checked; paper.md and agent-paper.md retain numeric prose citations. Schema snapshots are attributed official instructions/format evidence, not authored research.

**Git transport:** bundled original .gitignore bytes are immutable and can ignore their own copied paper/ and submissions/ descendants. A publisher must explicitly force-add every path in pinned-inputs.json when first staging this package, then independently verify all 50 files from the public Git archive. Do not rewrite copied .gitignore or any scientific blob to change that behavior. The root .gitattributes marks every bundled blob -text (including JSON/CSV) so LF/CRLF normalization cannot break archival hashes. No Git operation is performed here.

42 computational files belong exactly to H {args.expected_code_commit}; eight paper/TeX/builder/metadata files belong exactly to release {args.canonical_content_commit}. Historical README/review/provenance text reflects its stated source revision rather than current operational venue state. The public audit/ files here are specifically those already included in the immutable computational manifest; unrelated internal or private audit material is excluded. Original source PDFs and personal operational receipts are not bundled.

Model and token use are unknown, not estimated. All new venue gates remain false; a separate authorized client must verify this study's own final review release/closure immediately before a formal agent action. No generic prior-study acceptance can satisfy it. The original Taylor byline and scientific disclosures remain in the bundled canonical paper, while this separate authorized edition credits Lattice Audit Agent and Taylor as human operator.
"""
    attrs = "* text=auto eol=lf\n*.json -text\n*.csv -text\n*.png binary\n*.pdf binary\nreproduction/canonical/** -text\nreproduction/canonical/** whitespace=-blank-at-eol\n"
    products = {"paper.md": paper.encode(), "agent-paper.md": paper.encode(), "metadata.json": encode(metadata),
                "README.md": readme.encode(), "reproduction/README.md": reproduction.encode(),
                "reproduction/adapter-checks.json": encode(checks), "reproduction/canonical-preservation-v1.0.0.json": encode(checks),
                "reproduction/submission-context.json": encode(context), ".gitattributes": attrs.encode(),
                ".gitignore": b"__pycache__/\n*.pyc\n.private/\n",
                "LICENSE-CODE": source["reproduction/canonical/LICENSE-CODE"],
                "LICENSE-MANUSCRIPT": source["reproduction/canonical/LICENSE-MANUSCRIPT"]}
    for name, data in products.items():
        safe(name, data)
    if Path(__file__).read_bytes() != SCRIPT_BYTES or (ROOT / "reproduction/agentpub-paper-schema.json").read_bytes() != schema_raw:
        raise ValueError("Adapter/schema changed during preparation")
    if inputs(args)[0] != source:
        raise ValueError("Source bytes changed during preparation")
    for name, data in products.items():
        target = ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    outgoing.mkdir(parents=True, exist_ok=True)
    (outgoing / "ion-acoustic-agentpub-payload.json").write_bytes(encode(payload))
    (outgoing / "ion-acoustic-aaes-registration.json").write_bytes(encode(registration))
    assert all((ROOT / name).read_bytes() == data for name, data in products.items())
    print(json.dumps({"prepared": True, "files": 50, "math": len(blocks['math']), "equations": len(tags),
                      "figures": 2, "references": 5, "body_regex_words": body_words,
                      "max_section_UTF16": max(c['UTF16_code_units'] for c in caps.values()),
                      "payload_sha256": checks['agentpub_payload_sha256'], "gates_open": False}))


if __name__ == "__main__":
    main()

