import { useState } from "react";

type Props = {
  data: string[];
};

export function List({ data }: Props) {
  const [index, setIndex] = useState(0);

  const handleClick = (i: number) => {
    setIndex(i);
  }
  return (
    <ul className="list-group">
      {data.map((elemento, i) => (
        <li
          onClick={() => handleClick (i)}
          key={elemento}
          className={`list-group-item ${index == i ? 'active' : ''}`}
        >
          {elemento}
        </li>
      ))}
    </ul>
  );
}
