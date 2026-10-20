# Academic collection fixtures

Six real ACL records and eleven pinned writing-reference entries from collection run 39395351921. The six original paper selections are retained.

`plan.json` records immutable repository revisions and whole-file SHA256 values. `records.json` contains the selected XML paper elements, serialized with ElementTree; each record includes its parent source-file hash and the hash of the serialized fixture. These are source-replay fixtures, not generated prose.

D16-1264 has no abstract in the pinned XML. `abstract-overrides.json` contains the abstract from page 1 of the same paper's publisher PDF, checked visually on 2026-10-20. It is an attributed, curated excerpt, not a model-generated reconstruction or automatic PDF extraction. Its title, authors, source URL and text digest are checked before use. XML text takes precedence whenever present.

ACL abstracts: original authors listed in the plan; CC BY 4.0 for these 2016–2020 ACL publications. See https://aclanthology.org/faq/#what-is-the-copyright-for-materials-in-the-acl-anthology . XML serialization and removal of unrelated paper records are the only fixture changes. The repository's MIT license covers the collector code, not a relicensing of upstream material. Writing-skill text is fetched for inspection and not copied into this fixture directory.
