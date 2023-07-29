package benchmark_test

import (
	"testing"
)

type Struct struct {
	field1 int
	field2 float32
	field3 float64
	field4 complex64
	field5 complex128
}

func (f Struct) CopyReceiver() {
	//fmt.Sprintf("%d, %g, %g, %g, %g", f.field1, f.field2, f.field3, f.field4, f.field5)
}

func (f *Struct) PointerReceiver() {
	//fmt.Sprintf("%d, %g, %g, %g, %g", f.field1, f.field2, f.field3, f.field4, f.field5)
}

func BenchmarkCopyReceiver(b *testing.B) {
	data := Struct{}

	b.StartTimer()
	for i := 0; i < b.N; i++ {
		data.CopyReceiver()
	}
}

func BenchmarkPointerReceiver(b *testing.B) {
	data := Struct{}

	b.StartTimer()
	for i := 0; i < b.N; i++ {
		data.PointerReceiver()
	}
}
