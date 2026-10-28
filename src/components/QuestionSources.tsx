import type { Question } from '../domain/types';

export default function QuestionSources({ question }: { question: Question }) {
  return <div className="question-sources"><p>Nguồn slide: {question.source_reference.map(s => `${s.title}, tr. ${s.pdf_page}`).join(' · ')}</p>
    {question.supplemental_sources?.map(source => <p key={source.url}><b>Bổ sung ngoài slide:</b> <a href={source.url} target="_blank" rel="noreferrer">{source.title}</a> — {source.note}</p>)}
  </div>;
}
