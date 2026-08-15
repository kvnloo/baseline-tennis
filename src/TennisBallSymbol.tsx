type TennisBallSize = 'xs' | 'sm' | 'md' | 'lg' | 'hero'

type Props = {
  size?: TennisBallSize
  motion?: 'none' | 'hover' | 'bounce'
  glow?: boolean
  className?: string
  label?: string
}

export function TennisBallSymbol({
  size = 'sm',
  motion = 'hover',
  glow = true,
  className = '',
  label,
}: Props) {
  const assetMode = glow ? 'glow' : 'day'

  return (
    <span
      className={`tennis-ball tennis-ball--${size} tennis-ball--${motion} ${glow ? 'tennis-ball--glow' : ''} ${className}`}
      role={label ? 'img' : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
    >
      <span className="tennis-ball__shadow" />
      <img
        src={`./tennis-ball/tennis-ball-${assetMode}-256.webp`}
        srcSet={`./tennis-ball/tennis-ball-${assetMode}-256.webp 256w, ./tennis-ball/tennis-ball-${assetMode}-512.webp 512w, ./tennis-ball/tennis-ball-${assetMode}-1024.webp 1024w`}
        sizes={size === 'hero' ? '(max-width: 600px) 104px, 168px' : '64px'}
        alt=""
        draggable={false}
      />
    </span>
  )
}
